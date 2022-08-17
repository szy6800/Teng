const parser = require("@babel/parser");
// 为parser提供模板引擎
const template = require("@babel/template").default;
// 遍历AST
const traverse = require("@babel/traverse").default;
// 操作节点，比如判断节点类型，生成新的节点等
const types = require("@babel/types");
// 将语法树转换为源代码
const generator = require("@babel/generator");
// 操作文件
const fs = require("fs");

var k = function (e) {
    for (var t = 66, n = [], r = 0; r < e.length; r++) {
        var i = 24 ^ e.charCodeAt(r) ^ t;
        n.push(String.fromCharCode(i));
        t = i;
    }

    return n.join("");
};

let vmp_bin = "AxjgB5MAnACoAJwBpAAAABAAIAKcAqgAMAq0AzRJZAZwUpwCqACQACACGAKcBKAAIAOcBagAIAQYAjAUGgKcBqFAuAc5hTSHZAZwqrAIGgA0QJEAJAAYAzAUGgOcCaFANRQ0R2QGcOKwChoANECRACQAsAuQABgDnAmgAJwMgAGcDYwFEAAzBmAGcSqwDhoANECRACQAGAKcD6AAGgKcEKFANEcYApwRoAAxB2AGcXKwEhoANECRACQAGAKcE6AAGgKcFKFANEdkBnGqsBUaADRAkQAkABgCnBagAGAGcdKwFxoANECRACQAGAKcGKAAYAZx+rAZGgA0QJEAJAAYA5waoABgBnIisBsaADRAkQAkABgCnBygABoCnB2hQDRHZAZyWrAeGgA0QJEAJAAYBJwfoAAwFGAGcoawIBoANECRACQAGAOQALAJkAAYBJwfgAlsBnK+sCEaADRAkQAkABgDkACwGpAAGAScH4AJbAZy9rAiGgA0QJEAJACwI5AAGAScH6AAkACcJKgAnCWgAJwmoACcJ4AFnA2MBRAAMw5gBnNasCgaADRAkQAkABgBEio0R5EAJAGwKSAFGACcKqAAEgM0RCQGGAYSATRFZAZzshgAtCs0QCQAGAYSAjRFZAZz1hgAtCw0QCQAEAAgB7AtIAgYAJwqoAASATRBJAkYCRIANEZkBnYqEAgaBxQBOYAoBxQEOYQ0giQKGAmQABgAnC6ABRgBGgo0UhD/MQ8zECALEAgaBxQBOYAoBxQEOYQ0gpEAJAoYARoKNFIQ/zEPkAAgChgLGgkUATmBkgAaAJwuhAUaCjdQFAg5kTSTJAsQCBoHFAE5gCgHFAQ5hDSCkQAkChgBGgo0UhD/MQ+QACAKGAsaCRQCOYGSABoAnC6EBRoKN1AUEDmRNJMkCxgFGgsUPzmPkgAaCJwvhAU0wCQFGAUaCxQGOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQMOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQSOZISPzZPkQAaCJwvhAU0wCQFGAkSAzRBJAlz/B4FUAAAAwUYIAAIBSITFQkTERwABi0GHxITAAAJLwMSGRsXHxMZAAk0Fw8HFh4NAwUABhU1EBceDwAENBcUEAAGNBkTGRcBAAFKAAkvHg4PKz4aEwIAAUsACDIVHB0QEQ4YAAsuAzs7AAoPKToKDgAHMx8SGQUvMQABSAALORoVGCQgERcCAxoACAU3ABEXAgMaAAsFGDcAERcCAxoUCgABSQAGOA8LGBsPAAYYLwsYGw8AAU4ABD8QHAUAAU8ABSkbCQ4BAAFMAAktCh8eDgMHCw8AAU0ADT4TGjQsGQMaFA0FHhkAFz4TGjQsGQMaFA0FHhk1NBkCHgUbGBEPAAFCABg9GgkjIAEmOgUHDQ8eFSU5DggJAwEcAwUAAUMAAUAAAUEADQEtFw0FBwtdWxQTGSAACBwrAxUPBR4ZAAkqGgUDAwMVEQ0ACC4DJD8eAx8RAAQ5GhUYAAFGAAAABjYRExELBAACWhgAAVoAQAg/PTw0NxcQPCQ5C3JZEBs9fkcnDRcUAXZia0Q4EhQgXHojMBY3MWVCNT0uDhMXcGQ7AUFPHigkQUwQFkhaAkEACjkTEQspNBMZPC0ABjkTEQsrLQ==";
let opcode = [];
for (let t = atob(vmp_bin), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), i = 2; i < n + 2; i += 2) {
    opcode.push(t.charCodeAt(i) << 8 | t.charCodeAt(i + 1));
}
opcode.push(0);
let opstr = [];
for (let t = atob(vmp_bin), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), a = n + 2; a < t.length;) {
    var c = t.charCodeAt(a) << 8 | t.charCodeAt(a + 1),
        u = t.slice(a + 2, a + 2 + c);
    opstr.push(k(u));
    a += c + 2;
}

let ast = parser.parse("");
ast.program.body.push(types.variableDeclaration("var", [
    types.variableDeclarator(types.identifier('global_0')),
    types.variableDeclarator(types.identifier('global_1')),
    types.variableDeclarator(types.identifier('global_2')),
    types.variableDeclarator(types.identifier('global_3'))
]));

function get_blockstatement(pc, Local, blockstatement){
    let Stack = [];
    while (opcode[pc] !== 0){
        let t, s, i, h, a, c, n;
        switch ((61440 & opcode[pc]) >> 12) {
            case 0:
                break;
            case 1:
                break;
            case 2:
                break;
            case 3:
                break;
            case 4:
                break;
            case 5:
                break;
            case 6:
                break;
            case 7:
                break;
            case 8:
                break;
            case 9:
                t = (4095 & opcode[pc]) >> 10;
                s = (1023 & opcode[pc]) >> 8;
                i = 1023 & opcode[pc];
                h = 63 & opcode[pc];
                switch (t) {
                    case 0:
                        Stack.push(types.identifier('global_' + s));
                        pc++;
                        break;

                    case 1:
                        break;

                    case 2:
                        break;

                    case 3:
                        Stack.push(types.stringLiteral(opstr[h]));
                        pc++;
                        break
                }
                break;
            case 10:
                t = (4095 & opcode[pc]) >> 10;
                a = (1023 & opcode[pc]) >> 8;
                c = (255 & opcode[pc]) >> 6;
                switch (t) {
                    case 0:
                        break;
                    case 1:
                        s = Stack.pop(), i = Stack.pop();
                        blockstatement.push(
                            types.expressionStatement(
                                types.assignmentExpression(
                                    "=",
                                    types.memberExpression(
                                        types.identifier('global_' + c),
                                        s,
                                        true
                                    ),
                                    i
                                )
                            )
                        );
                        pc++;
                        break;
                    case 2:
                        h = Stack.pop();
                        blockstatement.push(types.expressionStatement(types.assignmentExpression("=", types.identifier('global_' + a), types.callExpression(types.identifier('eval'), [h]))));
                        pc++;
                        break;
                }
                break;
            case 11:
                break;
            case 12:
                break;
            case 13:
                break;
            case 14:
                let into_code = 4095 & opcode[pc];
                ast.program.body.push(types.functionDeclaration(types.identifier('_0x' + into_code), [], types.blockStatement([])));
                blockstatement.push(types.expressionStatement(types.assignmentExpression("=", types.identifier('global_3'), types.identifier('_0x' + into_code))));
                pc++;
                break;
            case 15:
                break;
        }
    }
    return blockstatement
}

ast.program.body.push(types.expressionStatement(types.callExpression(types.functionExpression(null, [], types.blockStatement(get_blockstatement(0, [], []))), [])));

let code = generator.default(ast).code;
console.log(code);