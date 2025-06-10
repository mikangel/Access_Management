# simple_nfc_web.py - 기존 Python 코드 + 웹 연동
import ctypes
import time
import json
import os
import threading
from ctypes import c_int, c_ubyte, c_uint, POINTER, byref
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# 🔧 설정 구역 - 여기만 수정하세요
EMPLOYEE_DB = {
    # 카드ID(10진수): {"name": "이름", "team": "팀명"}
    # 주의: team명은 웹페이지의 select 옵션과 정확히 일치해야 합니다!
    "1566783408": {"name": "임정환", "team": "IT자체감사팀"},
    "9876543210": {"name": "이영희", "team": "시스템팀"}, 
    "5555666677": {"name": "박민수", "team": "보안팀"},
    "1111222233": {"name": "정민호", "team": "네트워크팀"},
    "4444555566": {"name": "최영진", "team": "데이터팀"}
    # 새 사원 추가 방법: "카드ID": {"name": "홍길동", "team": "네트워크팀"}
    # 💡 team 값은 반드시 다음 중 하나여야 함:
    # "IT운영팀", "시스템팀", "보안팀", "네트워크팀", "데이터팀"
}

# 웹 서버 포트 (웹에서 http://localhost:8080 으로 접근)
WEB_PORT = 8080

# 전역 변수
latest_card_data = None
is_reading = False

class NFCWebHandler(BaseHTTPRequestHandler):
    """웹 요청 처리"""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/nfc/latest':
            # 최신 카드 정보 반환
            global latest_card_data
            if latest_card_data:
                response = latest_card_data
                latest_card_data = None  # 한 번 읽으면 초기화
            else:
                response = {"cardId": None}
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/nfc/status':
            # NFC 상태
            response = {
                "isRunning": is_reading,
                "message": "NFC 읽기 실행 중" if is_reading else "NFC 준비됨"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        else:
            self.send_error(404)
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"success": True, "message": "요청 처리됨"}
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        # 로그 출력 최소화
        pass

def nfc_reader_worker():
    """NFC 리더 워커 - 기존 코드 기반"""
    global latest_card_data, is_reading
    
    try:
        print("🔌 NFC 리더기 연결 중...")
        
        # DLL 로드 (경로 수정 필요)
        dll = ctypes.CDLL('./ComPro.dll')
        
        # 함수 정의 (기존 코드와 동일)
        dll.lc_init_ex.argtypes = [c_int, ctypes.c_char_p, ctypes.c_long]
        dll.lc_init_ex.restype = c_int
        dll.lc_exit.argtypes = [c_int]
        dll.lc_exit.restype = c_int
        dll.lc_setANT.argtypes = [c_int, c_ubyte]
        dll.lc_setANT.restype = c_int
        dll.lc_card.argtypes = [c_int, c_ubyte, POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_uint), POINTER(c_ubyte)]
        dll.lc_card.restype = c_int
        dll.lc_beep.argtypes = [c_int, c_uint]
        dll.lc_beep.restype = c_int
        
        # 리더기 연결
        hdev = dll.lc_init_ex(2, b"", 0)
        if hdev == -1:
            print("❌ 리더기 연결 실패")
            return
        
        print(f"✅ 리더기 연결 성공 (핸들: {hdev})")
        dll.lc_setANT(hdev, 1)
        dll.lc_beep(hdev, 10)  # 준비 완료 비프음
        
        print("📡 카드 대기 중...")
        
        is_reading = True
        last_uid = None
        
        while is_reading:
            snr = (c_ubyte * 9)()
            sn_len = c_ubyte()
            tag = c_uint()
            sak = c_ubyte()
            
            res = dll.lc_card(hdev, 1, snr, byref(sn_len), byref(tag), byref(sak))
            
            if res == 0:
                uid = ''.join(f"{snr[i]:02X}" for i in range(sn_len.value))
                if uid != last_uid:
                    uid_decimal = str(int(uid, 16))
                    
                    # 사원 정보 조회
                    employee = EMPLOYEE_DB.get(uid_decimal)
                    
                    # 웹으로 전달할 데이터 준비
                    latest_card_data = {
                        "cardId": uid_decimal,
                        "cardIdHex": uid,
                        "employee": employee,
                        "success": employee is not None,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # 콘솔 출력
                    print(f"✅ 카드 감지: {uid} ({uid_decimal})")
                    if employee:
                        print(f"👤 {employee['name']} ({employee['team']})")
                    else:
                        print(f"⚠️  등록되지 않은 카드 (UID: {uid_decimal})")
                    
                    dll.lc_beep(hdev, 10)  # 비프음
                    last_uid = uid
            else:
                last_uid = None
                
            time.sleep(0.3)
            
        dll.lc_exit(hdev)
        print("🛑 NFC 리더 종료")
        
    except Exception as e:
        print(f"❌ NFC 리더 오류: {e}")
        is_reading = False

def start_web_server():
    """웹 서버 시작"""
    try:
        server = HTTPServer(('localhost', WEB_PORT), NFCWebHandler)
        print(f"🌐 웹 서버 시작: http://localhost:{WEB_PORT}")
        server.serve_forever()
    except Exception as e:
        print(f"❌ 웹 서버 오류: {e}")

def print_usage():
    """사용법 출력"""
    print("=" * 60)
    print("🚀 농협 운영실 출입관리 NFC 서비스")
    print("=" * 60)
    print(f"📡 NFC 리더: 카드 대기 중")
    print(f"🌐 웹 서버: http://localhost:{WEB_PORT}")
    print()
    print("📋 사용 방법:")
    print("1. 웹 페이지에서 '카드 태그' 버튼 클릭")
    print("2. 사원증을 NFC 리더기에 태그")
    print("3. 자동으로 사원 정보가 입력됨")
    print()
    print("⚙️  새 사원 등록:")
    print("   - 이 파일의 EMPLOYEE_DB에 추가")
    print("   - 형식: \"카드ID\": {\"name\": \"이름\", \"team\": \"팀명\"}")
    print()
    print("🛑 종료: Ctrl+C")
    print("=" * 60)

def main():
    """메인 함수"""
    print_usage()
    
    # NFC 리더 스레드 시작
    nfc_thread = threading.Thread(target=nfc_reader_worker, daemon=True)
    nfc_thread.start()
    
    # 웹 서버 시작 (메인 스레드에서)
    try:
        start_web_server()
    except KeyboardInterrupt:
        print("\n🛑 서비스를 종료합니다...")
        global is_reading
        is_reading = False

if __name__ == "__main__":
    main()

# 📝 사용법:
# 1. 이 파일을 ComPro.dll과 같은 폴더에 저장
# 2. 터미널에서 실행: python simple_nfc_web.py
# 3. 웹 페이지에서 카드 태그 버튼 클릭
# 4. 사원증 태그하면 자동 입력됨

# 🔧 새 사원 추가 방법:
# EMPLOYEE_DB에 다음 형식으로 추가:
# "카드의10진수ID": {"name": "사원이름", "team": "소속팀"}

# 📋 사용 가능한 팀 목록 (웹페이지와 정확히 일치해야 함):
# - "IT운영팀"
# - "시스템팀" 
# - "보안팀"
# - "네트워크팀"
# - "데이터팀"

# 💡 새 팀을 추가하려면:
# 1. register.html의 <select name="witness_team"> 옵션에 추가
# 2. 이 파일의 EMPLOYEE_DB에서 해당 팀명 사용

# ⚠️  주의사항:
# - ComPro.dll 파일이 같은 폴더에 있어야 함
# - NFC 리더기가 USB에 연결되어 있어야 함
# - 포트 8080이 사용 중이면 WEB_PORT 변경
# - 팀명은 대소문자까지 정확히 일치해야 자동 선택됨