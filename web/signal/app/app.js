const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser');
const ini = require('iniparser');
const xml2js = require('xml2js');
const properties = require('properties');
const yaml = require('js-yaml');
const cp = require('child_process')
const path = require('path');
const session = require('express-session');

const app = express();
const port = process.env.PORT || 80;

// 设置存储配置
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });


app.use(express.static(path.join(__dirname, 'public')));
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(session({
	secret: 'welcome',//
	resave: false,
	saveUninitialized: false,
	cookie: {
		maxAge: 3600000
	}
}))

let output = '';

app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.post('/convert', upload.single('configFile'), (req, res) => {
	if (!req.file) {
		return res.status(400).send('No file uploaded.');
	}
	if(req.body.format!="yaml"){
		return res.status(404).send("该功能暂未开始使用.");
	}
	const fileExtension = path.extname(req.file.originalname).toLowerCase();
	const fileBuffer = req.file.buffer.toString('utf8');


	if (fileExtension === '.ini') {
		// 处理 INI 文件
		const parsedData = ini.parseString(fileBuffer);
		output = yaml.dump(parsedData);
	} else if (fileExtension === '.xml') {
		// 处理 XML 文件
		xml2js.parseString(fileBuffer, (err, result) => {
			if (err) {
				return res.status(500).send('Error parsing XML.');
			}
			output = yaml.dump(result);
		});
	} else if (fileExtension === '.properties') {
		// 处理 Properties 文件
		properties.parse(fileBuffer, (err, parsedData) => {
			if (err) {
				console.error('Error parsing properties file:', err);
				return res.status(500).send('Error parsing properties file.');
			}
			output = yaml.dump(parsedData);
		});
	} else if (fileExtension === '.yaml') {
		// 处理 YAML 文件
		try {
			// 尝试解析 YAML 文件
			const yamlData = yaml.load(fileBuffer);
			// 如果成功解析，yamlData 变量将包含 YAML 文件的内容
			output = yaml.dump(yamlData);
		} catch (e) {
			return res.status(400).send('Invalid YAML format: ' + e.message);
		}
	}

	if (output) {
		let name = 'ctfer';
		const yamlData = yaml.load(output);
		if (yamlData && yamlData.name) {
			 name = yamlData.name;
		}
		req.session.outputData=name;
		req.session.outputData=output;
		res.render('preview', { name: name,output: output }); // 渲染 preview.ejs 模板
	} else {
		res.status(400).send('Unsupported format.')
	}
});
app.get('/download', (req, res) => {
	if (output) {
		const outputData = req.session.outputData;

		// 设置响应头，指定文件的内容类型为YAML
		res.setHeader('Content-Type', 'application/x-yaml');
		// 设置响应头，指定文件名
		res.setHeader('Content-Disposition', 'attachment; filename="output.yaml"');

		// 将转换后的文件内容发送给客户端
		res.send(outputData);
	} else {
		res.status(404).send('File not found.');
	}
});
app.get('/flag',(req, res) => {
	if(req.session.name=='admin'){
		cp.execFile('/readflag', (err, stdout, stderr) => {
			if (err) {
				console.error('Error:', err);
				return res.status(404).send('File not found.');
			}
			res.send(stdout);
		})
	} else {
		res.status(403).send('Permission denied.');
	}
})

app.listen(port, () => {
	console.log(`App is running on port ${port}`)
})
