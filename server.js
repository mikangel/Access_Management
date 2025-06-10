const express = require('express');
const mysql = require('mysql2');
const path = require('path');
const fs = require('fs');
// ⛔️ 사용하지 않는 fs-extra 모듈은 제거해도 됩니다.
// const fse = require('fs-extra'); 

// ✅ mysqldump, openssl 등 시스템 명령어를 실행하기 위해 필요합니다.
const { exec } = require('child_process');

const app = express();
const PORT = 3000;

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.json());

// DB 연결
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'MyNewPass123!',
  database: 'access_log' 
});

db.connect(err => {
  if (err) {
    console.error('DB 연결 실패:', err);
    return;
  }
  console.log('MySQL 연결 성공!');
});

// --- 비밀번호 관련 API ---

const passwordFilePath = path.join(__dirname, 'public', 'password.json');

// [로그인] API
app.post('/api/login', (req, res) => {
  const { password: submittedPassword } = req.body;
  fs.readFile(passwordFilePath, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ message: '서버 설정 오류입니다.' });
    try {
      const storedPassword = JSON.parse(data).password;
      if (submittedPassword === storedPassword) {
        res.status(200).json({ message: '인증 성공' });
      } else {
        res.status(401).json({ message: '비밀번호가 올바르지 않습니다.' });
      }
    } catch (e) {
      res.status(500).json({ message: '서버 설정 파일이 손상되었습니다.' });
    }
  });
});

// [비밀번호 변경] API
app.post('/api/change-password', (req, res) => {
    const { currentPassword, newPassword } = req.body;
    fs.readFile(passwordFilePath, 'utf8', (err, data) => {
        if (err) return res.status(500).json({ message: '서버 오류' });
        try {
            const config = JSON.parse(data);
            if (currentPassword !== config.password) {
                return res.status(401).json({ message: '현재 비밀번호가 일치하지 않습니다.' });
            }
            config.password = newPassword;
            fs.writeFile(passwordFilePath, JSON.stringify(config, null, 2), (writeErr) => {
                if (writeErr) return res.status(500).json({ message: '비밀번호 저장에 실패했습니다.' });
                res.status(200).json({ message: '비밀번호가 성공적으로 변경되었습니다.' });
            });
        } catch(e) {
            res.status(500).json({ message: '서버 설정 파일이 손상되었습니다.' });
        }
    });
});


// --- 기존 데이터 관련 API (생략) ---
// ... (기존 /api/data, /api/register, /api/exit 등 API는 그대로 둡니다) ...
app.get('/api/data', (req, res) => {
  const sql = 'SELECT * FROM entry_log ORDER BY id DESC';
  db.query(sql, (err, results) => {
    if (err) return res.status(500).send('DB 조회 오류');
    res.json(results);
  });
});
app.post('/api/register', (req, res) => {
  const { name, company, reason, plan_number, entry_sign, witness_name, witness_team, witness_sign } = req.body;
  const sql = `INSERT INTO entry_log (name, company, reason, plan_number, entry_sign, witness_name, witness_team, witness_sign, entry_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, NOW())`;
  db.query(sql, [ name, company, reason, plan_number, entry_sign, witness_name, witness_team, witness_sign ], (err) => {
    if (err) return res.status(500).send('DB 오류');
    res.status(200).send('등록 완료');
  });
});
app.put('/api/exit/:id', (req, res) => {
  const { id } = req.params;
  const { exit_sign } = req.body;
  const sql = `UPDATE entry_log SET exit_time = NOW(), exit_sign = ? WHERE id = ? AND exit_time IS NULL`;
  db.query(sql, [exit_sign, id], (err, result) => {
    if (err) { console.error(err); return res.status(500).send('퇴실 처리 오류'); }
    res.send('퇴실 완료');
  });
});
app.get('/api/logs', (req, res) => {
  const date = req.query.date;
  const sql = `SELECT * FROM entry_log WHERE DATE(entry_time) = ?`;
  db.query(sql, [date], (err, results) => {
    if (err) return res.status(500).send('조회 실패');
    res.json(results);
  });
});
app.put('/api/verify/:id', (req, res) => {
  const { id } = req.params;
  const { checker_name, checker_team, checker_sign } = req.body;
  const sql = `UPDATE entry_log SET checker_name = ?, checker_team = ?, checker_sign = ? WHERE id = ?`;
  db.query(sql, [checker_name, checker_team, checker_sign, id], (err) => {
    if (err) return res.status(500).send('업데이트 실패');
    res.send('책임자 확인 완료');
  });
});
app.get('/api/report', (req, res) => {
  const { from, to } = req.query;
  const sql = `SELECT * FROM entry_log WHERE DATE(entry_time) BETWEEN ? AND ? ORDER BY entry_time ASC`;
  db.query(sql, [from, to], (err, results) => {
    if (err) return res.status(500).send('보고서 조회 실패');
    res.json(results);
  });
});


// ⛔️ [삭제] 기존 파일 시스템 백업 API는 삭제합니다.
/*
app.get('/api/backup-now', (req, res) => { ... });
*/


// ✅ [추가] settings.html을 위한 새로운 MySQL 백업 API
app.post('/api/backup/mysql', (req, res) => {
  // ⚠️ 보안 경고: 실제 운영 환경에서는 클라이언트로부터 DB 접속 정보를 직접 받는 것은 매우 위험합니다.
  // 이 코드는 데모 목적으로 작성되었으며, 실제 환경에서는 서버의 환경 변수나 보안 설정 파일을 사용해야 합니다.
  const { host, user, password, database, table, backupPath, encrypt, encryptionKey } = req.body;

  // 1. 백업 폴더가 없으면 생성
  if (!fs.existsSync(backupPath)) {
    try {
      fs.mkdirSync(backupPath, { recursive: true });
    } catch (err) {
      return res.status(500).json({ message: `백업 폴더 생성에 실패했습니다: ${err.message}`});
    }
  }

  // 2. 백업 파일명 및 전체 경로 생성
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backupFile = `${table}_backup_${timestamp}.sql`;
  const backupFilePath = path.join(backupPath, backupFile);

  // 3. mysqldump 명령어 생성
  // --password 인자 대신 MYSQL_PWD 환경변수를 사용하면 비밀번호가 프로세스 목록에 노출되지 않아 더 안전합니다.
  let command;
  const env = { ...process.env, MYSQL_PWD: password };

  const dumpCommand = `mysqldump --host=${host} --user=${user} ${database} ${table}`;

  if (encrypt) {
    // 암호화 옵션이 켜진 경우: mysqldump 결과를 openssl로 파이핑하여 암호화
    const encryptedFilePath = `${backupFilePath}.enc`;
    command = `${dumpCommand} | openssl enc -aes-256-cbc -salt -pbkdf2 -k "${encryptionKey}" -out "${encryptedFilePath}"`;
  } else {
    // 암호화 옵션이 꺼진 경우: 일반적인 sql 파일로 저장
    command = `${dumpCommand} > "${backupFilePath}"`;
  }

  console.log('실행될 백업 명령어:', dumpCommand); // 비밀번호 제외한 명령어 로그

  // 4. 백업 명령어 실행
  exec(command, { env }, (error, stdout, stderr) => {
    if (error) {
      console.error('백업 실패:', stderr);
      return res.status(500).json({ message: `백업 실행 중 오류가 발생했습니다: ${stderr}` });
    }
    console.log('백업 성공:', stdout);
    res.status(200).json({ message: '데이터베이스 백업을 성공적으로 완료했습니다.' });
  });
});


app.listen(PORT, () => {
  console.log(`http://localhost:${PORT} 에서 서버 실행 중`);
});