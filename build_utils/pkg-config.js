var spawn = require('child_process').spawnSync;
var isWin = /^win/.test(process.platform);

var pkg_config_executable = "pkg-config" + (isWin) ? ".exe" : "";

var args = process.argv.slice(2);
//console.log('argv',args);

if (args.indexOf("--exists") != -1){
	console.log(require('child_process').spawnSync('pkg-config',args).status == 0 ? "1" : "0");
	return;
}else if (args.indexOf("--libs") != -1){
	console.log(require('child_process').spawnSync('pkg-config',args).output.join(' '));
}
else if (args.indexOf("--cflags") != -1){
	console.log(require('child_process').spawnSync('pkg-config',args).output.join(' '));
}
