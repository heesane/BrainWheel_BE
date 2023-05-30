const express = require('express');
const swaggerUi = require('swagger-ui-express');
const cors = require('cors');

const app = express();

app.use(cors());

app.get('/',(req,res)=>{
  res.send("Hello");
});

app.listen(80, () => {
  console.log('Example app listening on port 80!');
});