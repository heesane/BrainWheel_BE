const express = require('express');
const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');

const app = express();

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// API 엔드포인트 등록
app.get('/api/users', (req, res) => {
  // 사용자 목록 반환
});

app.listen(3001, () => {
  console.log('Example app listening on port 3001!');
});