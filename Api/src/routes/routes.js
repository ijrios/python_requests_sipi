const express = require('express');
const router = express.Router();
const spawn = require('child_process').spawn;
const jwt = require('jsonwebtoken');
const fs = require('fs');
const secret = process.env.SECRET;

const taskQueue = {};

async function runTask(name) {
    while (taskQueue[name] && taskQueue[name].length > 0) {
        const taskFn = taskQueue[name][0];
        await taskFn();
        await new Promise(resolve => setTimeout(resolve, 60 * 1000)); // 1 minuto de espera
        taskQueue[name].shift();
    }
}

async function executePythonScript(script, name, args = [], maxAttempts = 3, delay = 40000) {
    let attempts = 0;
    const logFilePath = `./log/${name}.txt`;

    const runScript = () => {
        return new Promise((resolve, reject) => {
        
            const process = spawn('python', [script, ...args], { stdio: ['ignore', 'pipe', 'pipe'] });
            const logStream = fs.createWriteStream(logFilePath, { flags: 'a' });

            process.stdout.on('data', (data) => {
                logStream.write(data);
            });

            process.stderr.on('data', (data) => {
                logStream.write(data);
            });

            process.on('error', (err) => {
                console.error(err);
                logStream.end();
                reject(err);
            });

            process.on('close', (code) => {
                logStream.end();
                if (code === 0) {
                    resolve();
                } else {
                    reject(new Error(`El script finalizó con código de salida ${code}`));
                }
            });
        });
    };

    while (attempts < maxAttempts) {
        try {
            await runScript();
            return; // Si el script se ejecuta correctamente, salimos de la función
        } catch (err) {
            attempts++;
            console.log(`Reintentando (${attempts}/${maxAttempts})...`);
            await new Promise(resolve => setTimeout(resolve, delay));
        }
    }

    throw new Error('Max attempts reached');
}

function verifyToken(req, res, next) {
    const bearerHeader = req.headers['authorization'];
    if (typeof bearerHeader !== 'undefined') {
        const bearerToken = bearerHeader.split(' ')[1];
        req.token = bearerToken;
        next();
    } else {
        res.sendStatus(403); // Forbidden
    }
}

function executeTask(name, taskFn) {
    if (!taskQueue[name]) {
        taskQueue[name] = [];
    }
    taskQueue[name].push(taskFn);

    if (taskQueue[name].length === 1) {
        runTask(name);
    }
}

router.get('/ObtenerToken', (req, res) => {
    const token = jwt.sign({_id: 487384653223}, secret);
    res.status(200).json({token});
});

router.get('/ruta2', verifyToken, (req, res) => {
    executeTask('LoginTask', async () => {
        console.log('Ejecutando la tarea de login');
        try {
            await executePythonScript('./scripts/pruebas.py', 'LoginScript');
            console.log('Script de login ejecutado con éxito');
        } catch (err) {
            console.error('Error al ejecutar el script login.py', err);
        }
    });
    res.status(200).send("Ejecución en proceso");
});

router.get('/muestra', (req, res) => {
    executeTask('LoginTask', async () => {
        console.log('Ejecutando la tarea de login');
        try {
            // await executePythonScript('./scripts/pruebas.py', 'LoginScript');
            console.log('Script de login ejecutado con éxito');
        } catch (err) {
            console.error('Error al ejecutar el script login.py', err);
        }
    });
    res.status(200).send("Ejecución en proceso");
});

router.get('/api/v3/RegistroMarca/:Id', (req, res) => {
    executeTask('Marcas', async () => {
        console.log('Ejecutando Marcas');
        const Id = req.params.Id;
  
        try {
          await executePythonScript('./scripts/Registro.py', 'RegistroMarca', [Id]);
          console.log('Script de registro ejecutado con éxito');
        } catch (err) {
            console.error('Error al ejecutar el script Registro.py', err);
        }
    });
    res.status(200).send("Ejecución en proceso");
  });

router.get('/api/v3/Vencimiento', (req, res) => {
    executeTask('Marcas', async () => {
        console.log('Ejecutando Marcas');
        const Id = req.params.Id;
  
        try {
          await executePythonScript('./scripts/Vencimiento.py', 'RegistroMarca', [Id]);
          console.log('Script de vencimiento ejecutado con éxito');
        } catch (err) {
            console.error('Error al ejecutar el script Vencimiento.py', err);
        }
    });
    res.status(200).send("Ejecución en proceso");
  });
  
  

module.exports = router;