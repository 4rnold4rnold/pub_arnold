const SwaggerParser = require('swagger-parser');

SwaggerParser.validate('swagger.json')
  .then(apiData => {
    const paths = apiData.paths;

    console.log('Paths:', paths);

    for (const path in paths) {
      console.log(`Path: ${path}`);
      const pathItem = paths[path];

      for (const method in pathItem) {
        console.log(`  Method: ${method}`);
        const operation = pathItem[method];
        console.log(`    Summary: ${operation.summary}`);
      }
    }
  })
  .catch(err => {
    console.error('Error:', err);
  });