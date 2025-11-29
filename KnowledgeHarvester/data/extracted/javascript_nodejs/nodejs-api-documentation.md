About this documentation | Node.js v25.2.1 Documentation






[Skip to content](#apicontent)



[Node.js](/ "Go back to the home page") 

* [About this documentation](documentation.html)
* [Usage and example](synopsis.html)




---


* [Assertion testing](assert.html)
* [Asynchronous context tracking](async_context.html)
* [Async hooks](async_hooks.html)
* [Buffer](buffer.html)
* [C++ addons](addons.html)
* [C/C++ addons with Node-API](n-api.html)
* [C++ embedder API](embedding.html)
* [Child processes](child_process.html)
* [Cluster](cluster.html)
* [Command-line options](cli.html)
* [Console](console.html)
* [Crypto](crypto.html)
* [Debugger](debugger.html)
* [Deprecated APIs](deprecations.html)
* [Diagnostics Channel](diagnostics_channel.html)
* [DNS](dns.html)
* [Domain](domain.html)
* [Environment Variables](environment_variables.html)
* [Errors](errors.html)
* [Events](events.html)
* [File system](fs.html)
* [Globals](globals.html)
* [HTTP](http.html)
* [HTTP/2](http2.html)
* [HTTPS](https.html)
* [Inspector](inspector.html)
* [Internationalization](intl.html)
* [Modules: CommonJS modules](modules.html)
* [Modules: ECMAScript modules](esm.html)
* [Modules: `node:module` API](module.html)
* [Modules: Packages](packages.html)
* [Modules: TypeScript](typescript.html)
* [Net](net.html)
* [OS](os.html)
* [Path](path.html)
* [Performance hooks](perf_hooks.html)
* [Permissions](permissions.html)
* [Process](process.html)
* [Punycode](punycode.html)
* [Query strings](querystring.html)
* [Readline](readline.html)
* [REPL](repl.html)
* [Report](report.html)
* [Single executable applications](single-executable-applications.html)
* [SQLite](sqlite.html)
* [Stream](stream.html)
* [String decoder](string_decoder.html)
* [Test runner](test.html)
* [Timers](timers.html)
* [TLS/SSL](tls.html)
* [Trace events](tracing.html)
* [TTY](tty.html)
* [UDP/datagram](dgram.html)
* [URL](url.html)
* [Utilities](util.html)
* [V8](v8.html)
* [VM](vm.html)
* [WASI](wasi.html)
* [Web Crypto API](webcrypto.html)
* [Web Streams API](webstreams.html)
* [Worker threads](worker_threads.html)
* [Zlib](zlib.html)




---


* [Code repository and issue tracker](https://github.com/nodejs/node)






# Node.js v25.2.1 documentation















* Node.js v25.2.1
* [Table of contents](#toc-picker) 

	+ [About this documentation](#about-this-documentation)
		- [Contributing](#contributing)
		- [Stability index](#stability-index)
		- [Stability overview](#stability-overview)
		- [JSON output](#json-output)
		- [System calls and man pages](#system-calls-and-man-pages)
* [Index](#gtoc-picker) 

	+ [About this documentation](documentation.html)
	+ [Usage and example](synopsis.html)
	+ [Index](index.html)


---



	+ [Assertion testing](assert.html)
	+ [Asynchronous context tracking](async_context.html)
	+ [Async hooks](async_hooks.html)
	+ [Buffer](buffer.html)
	+ [C++ addons](addons.html)
	+ [C/C++ addons with Node-API](n-api.html)
	+ [C++ embedder API](embedding.html)
	+ [Child processes](child_process.html)
	+ [Cluster](cluster.html)
	+ [Command-line options](cli.html)
	+ [Console](console.html)
	+ [Crypto](crypto.html)
	+ [Debugger](debugger.html)
	+ [Deprecated APIs](deprecations.html)
	+ [Diagnostics Channel](diagnostics_channel.html)
	+ [DNS](dns.html)
	+ [Domain](domain.html)
	+ [Environment Variables](environment_variables.html)
	+ [Errors](errors.html)
	+ [Events](events.html)
	+ [File system](fs.html)
	+ [Globals](globals.html)
	+ [HTTP](http.html)
	+ [HTTP/2](http2.html)
	+ [HTTPS](https.html)
	+ [Inspector](inspector.html)
	+ [Internationalization](intl.html)
	+ [Modules: CommonJS modules](modules.html)
	+ [Modules: ECMAScript modules](esm.html)
	+ [Modules: `node:module` API](module.html)
	+ [Modules: Packages](packages.html)
	+ [Modules: TypeScript](typescript.html)
	+ [Net](net.html)
	+ [OS](os.html)
	+ [Path](path.html)
	+ [Performance hooks](perf_hooks.html)
	+ [Permissions](permissions.html)
	+ [Process](process.html)
	+ [Punycode](punycode.html)
	+ [Query strings](querystring.html)
	+ [Readline](readline.html)
	+ [REPL](repl.html)
	+ [Report](report.html)
	+ [Single executable applications](single-executable-applications.html)
	+ [SQLite](sqlite.html)
	+ [Stream](stream.html)
	+ [String decoder](string_decoder.html)
	+ [Test runner](test.html)
	+ [Timers](timers.html)
	+ [TLS/SSL](tls.html)
	+ [Trace events](tracing.html)
	+ [TTY](tty.html)
	+ [UDP/datagram](dgram.html)
	+ [URL](url.html)
	+ [Utilities](util.html)
	+ [V8](v8.html)
	+ [VM](vm.html)
	+ [WASI](wasi.html)
	+ [Web Crypto API](webcrypto.html)
	+ [Web Streams API](webstreams.html)
	+ [Worker threads](worker_threads.html)
	+ [Zlib](zlib.html)


---



	+ [Code repository and issue tracker](https://github.com/nodejs/node)
* [Other versions](#alt-docs) 

	1. [25.x](https://nodejs.org/docs/latest-v25.x/api/documentation.html)
	2. [24.x **LTS**](https://nodejs.org/docs/latest-v24.x/api/documentation.html)
	3. [23.x](https://nodejs.org/docs/latest-v23.x/api/documentation.html)
	4. [22.x **LTS**](https://nodejs.org/docs/latest-v22.x/api/documentation.html)
	5. [21.x](https://nodejs.org/docs/latest-v21.x/api/documentation.html)
	6. [20.x **LTS**](https://nodejs.org/docs/latest-v20.x/api/documentation.html)
	7. [19.x](https://nodejs.org/docs/latest-v19.x/api/documentation.html)
	8. [18.x](https://nodejs.org/docs/latest-v18.x/api/documentation.html)
	9. [17.x](https://nodejs.org/docs/latest-v17.x/api/documentation.html)
	10. [16.x](https://nodejs.org/docs/latest-v16.x/api/documentation.html)
	11. [15.x](https://nodejs.org/docs/latest-v15.x/api/documentation.html)
	12. [14.x](https://nodejs.org/docs/latest-v14.x/api/documentation.html)
	13. [13.x](https://nodejs.org/docs/latest-v13.x/api/documentation.html)
	14. [12.x](https://nodejs.org/docs/latest-v12.x/api/documentation.html)
	15. [11.x](https://nodejs.org/docs/latest-v11.x/api/documentation.html)
	16. [10.x](https://nodejs.org/docs/latest-v10.x/api/documentation.html)
	17. [9.x](https://nodejs.org/docs/latest-v9.x/api/documentation.html)
	18. [8.x](https://nodejs.org/docs/latest-v8.x/api/documentation.html)
	19. [7.x](https://nodejs.org/docs/latest-v7.x/api/documentation.html)
	20. [6.x](https://nodejs.org/docs/latest-v6.x/api/documentation.html)
	21. [5.x](https://nodejs.org/docs/latest-v5.x/api/documentation.html)
	22. [4.x](https://nodejs.org/docs/latest-v4.x/api/documentation.html)
	23. [0.12.x](https://nodejs.org/docs/latest-v0.12.x/api/documentation.html)
	24. [0.10.x](https://nodejs.org/docs/latest-v0.10.x/api/documentation.html)
* [Options](#options-picker) 


	+ [View on single page](all.html)
	+ [View as JSON](documentation.json)
	+ [Edit on GitHub](https://github.com/nodejs/node/edit/main/doc/api/documentation.md)





---



Table of contents* [About this documentation](#about-this-documentation)
	+ [Contributing](#contributing)
	+ [Stability index](#stability-index)
	+ [Stability overview](#stability-overview)
	+ [JSON output](#json-output)
	+ [System calls and man pages](#system-calls-and-man-pages)


## About this documentation[#](#about-this-documentation)


Welcome to the official API reference documentation for Node.js!


Node.js is a JavaScript runtime built on the [V8 JavaScript engine](https://v8.dev/).


### Contributing[#](#contributing)


Report errors in this documentation in [the issue tracker](https://github.com/nodejs/node/issues/new). See
[the contributing guide](https://github.com/nodejs/node/blob/HEAD/CONTRIBUTING.md) for directions on how to submit pull requests.


### Stability index[#](#stability-index)


Throughout the documentation are indications of a section's stability. Some APIs
are so proven and so relied upon that they are unlikely to ever change at all.
Others are brand new and experimental, or known to be hazardous.


The stability indexes are as follows:


Stability: 0 - Deprecated. The feature may emit warnings. Backward
compatibility is not guaranteed.

Stability: 1 - Experimental. The feature is not subject to
[semantic versioning](https://semver.org/) rules. Non-backward compatible changes or removal may
occur in any future release. Use of the feature is not recommended in
production environments.Experimental features are subdivided into stages:

* 1.0 - Early development. Experimental features at this stage are unfinished
and subject to substantial change.
* 1.1 - Active development. Experimental features at this stage are nearing
minimum viability.
* 1.2 - Release candidate. Experimental features at this stage are hopefully
ready to become stable. No further breaking changes are anticipated but may
still occur in response to user feedback or the features' underlying
specification development. We encourage user testing and feedback so that
we can know that this feature is ready to be marked as stable.

Experimental features leave the experimental status typically either by
graduating to stable, or are removed without a deprecation cycle.



Stability: 2 - Stable. Compatibility with the npm ecosystem is a high
priority.

Stability: 3 - Legacy. Although this feature is unlikely to be removed and is
still covered by semantic versioning guarantees, it is no longer actively
maintained, and other alternatives are available.
Features are marked as legacy rather than being deprecated if their use does no
harm, and they are widely relied upon within the npm ecosystem. Bugs found in
legacy features are unlikely to be fixed.


Use caution when making use of Experimental features, particularly when
authoring libraries. Users may not be aware that experimental features are being
used. Bugs or behavior changes may surprise users when Experimental API
modifications occur. To avoid surprises, use of an Experimental feature may need
a command-line flag. Experimental features may also emit a [warning](process.html#event-warning).


### Stability overview[#](#stability-overview)




| API | Stability |
| --- | --- |
| [Assert](assert.html) | (2) Stable |
| [Async hooks](async_hooks.html) | (1) Experimental |
| [Asynchronous context tracking](async_context.html) | (2) Stable |
| [Buffer](buffer.html) | (2) Stable |
| [Child process](child_process.html) | (2) Stable |
| [Cluster](cluster.html) | (2) Stable |
| [Console](console.html) | (2) Stable |
| [Crypto](crypto.html) | (2) Stable |
| [Diagnostics Channel](diagnostics_channel.html) | (2) Stable |
| [DNS](dns.html) | (2) Stable |
| [Domain](domain.html) | (0) Deprecated |
| [File system](fs.html) | (2) Stable |
| [HTTP](http.html) | (2) Stable |
| [HTTP/2](http2.html) | (2) Stable |
| [HTTPS](https.html) | (2) Stable |
| [Inspector](inspector.html) | (2) Stable |
| [Modules: `node:module` API](module.html) | (1) .1 - Active development |
| [Modules: CommonJS modules](modules.html) | (2) Stable |
| [Modules: TypeScript](typescript.html) | (2) Stable |
| [OS](os.html) | (2) Stable |
| [Path](path.html) | (2) Stable |
| [Performance measurement APIs](perf_hooks.html) | (2) Stable |
| [Punycode](punycode.html) | (0) Deprecated |
| [Query string](querystring.html) | (2) Stable |
| [Readline](readline.html) | (2) Stable |
| [REPL](repl.html) | (2) Stable |
| [Single executable applications](single-executable-applications.html) | (1) .1 - Active development |
| [SQLite](sqlite.html) | (1) .1 - Active development. |
| [Stream](stream.html) | (2) Stable |
| [String decoder](string_decoder.html) | (2) Stable |
| [Test runner](test.html) | (2) Stable |
| [Timers](timers.html) | (2) Stable |
| [TLS (SSL)](tls.html) | (2) Stable |
| [Trace events](tracing.html) | (1) Experimental |
| [TTY](tty.html) | (2) Stable |
| [UDP/datagram sockets](dgram.html) | (2) Stable |
| [URL](url.html) | (2) Stable |
| [Util](util.html) | (2) Stable |
| [VM (executing JavaScript)](vm.html) | (2) Stable |
| [Web Crypto API](webcrypto.html) | (2) Stable |
| [Web Streams API](webstreams.html) | (2) Stable |
| [WebAssembly System Interface (WASI)](wasi.html) | (1) Experimental |
| [Worker threads](worker_threads.html) | (2) Stable |
| [Zlib](zlib.html) | (2) Stable |


### JSON output[#](#json-output)



Added in: v0.6.12

Every `.html` document has a corresponding `.json` document. This is for IDEs
and other utilities that consume the documentation.


### System calls and man pages[#](#system-calls-and-man-pages)


Node.js functions which wrap a system call will document that. The docs link
to the corresponding man pages which describe how the system call works.


Most Unix system calls have Windows analogues. Still, behavior differences may
be unavoidable.