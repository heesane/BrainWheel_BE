const express = require('express');
const swaggerUi = require('swagger-ui-express');


const app = express();


app.get('/',(req,res)=>{
  res.send("Hello");
});

// API 엔드포인트 등록
app.get('/api/users', (req, res) => {
  // 사용자 목록 반환
});

app.listen(3000, () => {
  console.log('Example app listening on port 3000!');
});