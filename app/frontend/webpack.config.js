const path = require('path');

module.exports = {
	entry: './src/index.js',  // Entry point of your application
	output: {
		path: path.resolve(__dirname, 'dist'),  // Output directory
		filename: 'bundle.js'  // Output bundle filename
	},
	// Other webpack configuration options go here
	resolve: {},

};