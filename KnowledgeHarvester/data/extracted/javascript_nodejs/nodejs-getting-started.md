Node.js — Introduction to Node.jsChange pageIntroduction to Node.jsGetting Started[Introduction to Node.js](/en/learn/getting-started/introduction-to-nodejs)[How much JavaScript do you need to know to use Node.js?](/en/learn/getting-started/how-much-javascript-do-you-need-to-know-to-use-nodejs)[Differences between Node.js and the Browser](/en/learn/getting-started/differences-between-nodejs-and-the-browser)[The V8 JavaScript Engine](/en/learn/getting-started/the-v8-javascript-engine)[An introduction to the npm package manager](/en/learn/getting-started/an-introduction-to-the-npm-package-manager)[ECMAScript 2015 (ES6) and beyond](/en/learn/getting-started/ecmascript-2015-es6-and-beyond)[Debugging Node.js](/en/learn/getting-started/debugging)[Fetching data with Node.js](/en/learn/getting-started/fetch)[WebSocket client with Node.js](/en/learn/getting-started/websocket)[Node.js, the difference between development and production](/en/learn/getting-started/nodejs-the-difference-between-development-and-production)[Profiling Node.js Applications](/en/learn/getting-started/profiling)[Node.js with WebAssembly](/en/learn/getting-started/nodejs-with-webassembly)[Security Best Practices](/en/learn/getting-started/security-best-practices)[Introduction to Userland Migrations](/en/learn/getting-started/userland-migrations)Command Line[Run Node.js scripts from the command line](/en/learn/command-line/run-nodejs-scripts-from-the-command-line)[How to use the Node.js REPL](/en/learn/command-line/how-to-use-the-nodejs-repl)[Output to the command line using Node.js](/en/learn/command-line/output-to-the-command-line-using-nodejs)[Accept input from the command line in Node.js](/en/learn/command-line/accept-input-from-the-command-line-in-nodejs)[How to read environment variables from Node.js](/en/learn/command-line/how-to-read-environment-variables-from-nodejs)HTTP[Anatomy of an HTTP Transaction](/en/learn/http/anatomy-of-an-http-transaction)Manipulating Files[Node.js file stats](/en/learn/manipulating-files/nodejs-file-stats)[Node.js File Paths](/en/learn/manipulating-files/nodejs-file-paths)[Reading files with Node.js](/en/learn/manipulating-files/reading-files-with-nodejs)[Writing files with Node.js](/en/learn/manipulating-files/writing-files-with-nodejs)[Working with file descriptors in Node.js](/en/learn/manipulating-files/working-with-file-descriptors-in-nodejs)[Working with folders in Node.js](/en/learn/manipulating-files/working-with-folders-in-nodejs)[How to work with Different Filesystems](/en/learn/manipulating-files/working-with-different-filesystems)Asynchronous Work[JavaScript Asynchronous Programming and Callbacks](/en/learn/asynchronous-work/javascript-asynchronous-programming-and-callbacks)[Asynchronous flow control](/en/learn/asynchronous-work/asynchronous-flow-control)[Discover Promises in Node.js](/en/learn/asynchronous-work/discover-promises-in-nodejs)[Discover JavaScript Timers](/en/learn/asynchronous-work/discover-javascript-timers)[Overview of Blocking vs Non-Blocking](/en/learn/asynchronous-work/overview-of-blocking-vs-non-blocking)[The Node.js Event Loop](/en/learn/asynchronous-work/event-loop-timers-and-nexttick)[The Node.js Event Emitter](/en/learn/asynchronous-work/the-nodejs-event-emitter)[Understanding process.nextTick()](/en/learn/asynchronous-work/understanding-processnexttick)[Understanding setImmediate()](/en/learn/asynchronous-work/understanding-setimmediate)[Don't Block the Event Loop](/en/learn/asynchronous-work/dont-block-the-event-loop)TypeScript[Introduction to TypeScript](/en/learn/typescript/introduction)[Running TypeScript Natively](/en/learn/typescript/run-natively)[Running TypeScript code using transpilation](/en/learn/typescript/transpile)[Running TypeScript with a runner](/en/learn/typescript/run)[Publishing a TypeScript package](/en/learn/typescript/publishing-a-ts-package)Modules[How to use streams](/en/learn/modules/how-to-use-streams)[Backpressuring in Streams](/en/learn/modules/backpressuring-in-streams)[Publishing a package](/en/learn/modules/publishing-a-package)[How to publish a Node-API package](/en/learn/modules/publishing-node-api-modules)[ABI Stability](/en/learn/modules/abi-stability)Diagnostics[User Journey](/en/learn/diagnostics/user-journey)[Memory](/en/learn/diagnostics/memory)[Live Debugging](/en/learn/diagnostics/live-debugging)[Poor Performance](/en/learn/diagnostics/poor-performance)[Flame Graphs](/en/learn/diagnostics/flame-graphs)Test Runner[Discovering Node.js's test runner](/en/learn/test-runner/introduction)[Using Node.js's test runner](/en/learn/test-runner/using-test-runner)[Mocking in tests](/en/learn/test-runner/mocking)[Collecting code coverage in Node.js](/en/learn/test-runner/collecting-code-coverage)# [Introduction to Node.js](#introduction-to-nodejs)


Node.js is an open-source and cross-platform JavaScript runtime environment. It is a popular tool for almost any kind of project!


Node.js runs the V8 JavaScript engine, the core of Google Chrome, outside of the browser. This allows Node.js to be very performant.


A Node.js app runs in a single process, without creating a new thread for every request. Node.js provides a set of asynchronous I/O primitives in its standard library that prevent JavaScript code from blocking. In addition, libraries in Node.js are generally written using non-blocking paradigms. Accordingly, blocking behavior is the exception rather than the norm in Node.js.


When Node.js performs an I/O operation, like reading from the network, accessing a database or the filesystem, instead of blocking the thread and wasting CPU cycles waiting, Node.js will resume the operations when the response comes back.


This allows Node.js to handle thousands of concurrent connections with a single server without introducing the burden of managing thread concurrency, which could be a significant source of bugs.


Node.js has a unique advantage because millions of frontend developers that write JavaScript for the browser are now able to write the server-side code in addition to the client-side code without the need to learn a completely different language.


In Node.js the new ECMAScript standards can be used without problems, as you don't have to wait for all your users to update their browsers - you are in charge of deciding which ECMAScript version to use by changing the Node.js version, and you can also enable specific experimental features by running Node.js with flags.


## [An Example Node.js Application](#an-example-nodejs-application)


The most common example Hello World of Node.js is a web server:


CJSESM
```
const { createServer } = require('node:http');

const hostname = '127.0.0.1';
const port = 3000;

const server = createServer((req, res) => {
 res.statusCode = 200;
 res.setHeader('Content-Type', 'text/plain');
 res.end('Hello World');
});

server.listen(port, hostname, () => {
 console.log(`Server running at http://${hostname}:${port}/`);
});

```
JavaScriptCopy to clipboardTo run this snippet, save it as a `server.js` file and run `node server.js` in your terminal.
If you use mjs version of the code, you should save it as a `server.mjs` file and run `node server.mjs` in your terminal.


This code first includes the Node.js [`http` module](https://nodejs.org/api/http.html).


Node.js has a fantastic [standard library](https://nodejs.org/api/), including first-class support for networking.


The `createServer()` method of `http` creates a new HTTP server and returns it.


The server is set to listen on the specified port and host name. When the server is ready, the callback function is called, in this case informing us that the server is running.


Whenever a new request is received, the [`request` event](https://nodejs.org/api/http.html#http_event_request) is called, providing two objects: a request (an [`http.IncomingMessage`](https://nodejs.org/api/http.html#http_class_http_incomingmessage) object) and a response (an [`http.ServerResponse`](https://nodejs.org/api/http.html#http_class_http_serverresponse) object).


Those 2 objects are essential to handle the HTTP call.


The first provides the request details. In this simple example, this is not used, but you could access the request headers and request data.


The second is used to return data to the caller.


In this case with:



```
res.statusCode = 200;

```
JavaScriptCopy to clipboard
we set the `statusCode` property to `200`, to indicate a successful response.


We set the `Content-Type` header:



```
res.setHeader('Content-Type', 'text/plain');

```
JavaScriptCopy to clipboard
and we close the response, adding the content as an argument to `end()`:



```
res.end('Hello World\n');

```
JavaScriptCopy to clipboard
If you haven't already done so, [download](https://nodejs.org/en/download) Node.js.

[NextHow much JavaScript do you need to know to use Node.js?](/en/learn/getting-started/how-much-javascript-do-you-need-to-know-to-use-nodejs)Reading Time3 minAuthors[F](https://github.com/flaviocopes)[P](https://github.com/potch)[MB](https://github.com/mylesborins)[R](https://github.com/RomainLanz)[V](https://github.com/virkt25)[T](https://github.com/Trott)[O](https://github.com/onel0p3z)[O](https://github.com/ollelauribostrom)[M](https://github.com/MarkPieszak)+10Contribute[Edit this page](https://github.com/nodejs/nodejs.org/blob/main/apps/site/pages/en/learn/getting-started/introduction-to-nodejs.md)Table of Contents1. [An Example Node.js Application](#an-example-nodejs-application)