const express = require('express');
const app = express();
const morgan = require('morgan');
const http = require('http')
const jwt = require('jsonwebtoken');
require('dotenv').config();


//Configuraciones
app.set('port', process.env.PORT || 3700);

const server = http.createServer(app);

//middlewaress
app.use(morgan('dev'));
app.use(express.urlencoded({extended: false}));
app.use(express.json());
 

//Rutas
app.use(require('./routes/routes'));


//Inicio del servidor
app.listen(app.get('port'), () => {
    console.log(`Servidor en puerto ${app.get('port')}`);
});