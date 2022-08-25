
function success(data) {
						if (data.code == 1 || data.code == "success") {
							if(data.secretKey){
								var obj = DES3.decrypt(data.result, data.secretKey);
								try{ obj = $.parseJSON(obj) }catch(e){ }
								data.result = obj;
							}
							if(opt.rollback){
								if(typeof opt.rollback === "function"){
									if(data.result== null && typeof data.description === "string"){
										try{
											opt.rollback($.parseJSON(data.description));
										}catch(e){
											$.WebSite.appendToView(item || "msg", e);
										}
									}else{
										opt.rollback(data.result);
									}
								}
							}
						} else {
							if(typeof opt.error === "function"){
								opt.error(data);
							} else {
								// 用户未登录

								if (data.code == -4) {
									if(typeof loginWindow == "function"){
										loginWindow();
									} else {
										$.WebSite.msg({
											msg: "用户未登录，请重新登录",
											type: 2
										})
									}
								}
								// 访问数据过于频繁，需要验证码验证

								else if (data.code == -11) {
									layer.open({
										type: 1,
										area: ['420px', '240px'], //宽高
										title: "访问受限",
										closeBtn: 0,
										btn: ['提交验证'],
										yes: function(index, layero){
											opt.param["antitheftImageCode"] = $("input#imageCode").val();
											if(opt.param["antitheftImageCode"] == ""){
												$.WebSite.msg({
													msg: "请输入验证码",
													type: 2
												});
												$("input#imageCode").css({"border": "1px solid red"});
												return;
											}
											$.WebSite.getData(opt);
											if(opt["$m"]){
												setTimeout(function(){
													$.WebSite.invoke(opt["$m"]["randomId"], "onloadMethod");
												}, 500);
											}
											layer.close(index);
										},
										content:
											'<div style="width: 400px margin: 5px auto;line-height: 30px;padding: 10px 20px">' +
											'<div>提示：' + data.description + '</div>' +
											'<div>验证码：<input id="imageCode" autocomplete="off" type="text" style="border:1px solid #ccc;"></div>' +
										'<div><img alt="图片验证码" id="codeImagePic" src="' + $svc.validImg + '?' + Math.random() + '" style="margin-left: 10px"></div>' +
										'</div>'
									});
									$("body").on("click", "img#codeImagePic", function(){
										$.WebSite.reloadCaptcha(this);
									})
								} else {
									/*$.WebSite.msg({
										msg: data.description||"数据解析异常",
										type: 2
									})*/
								}
							}
						}
					}


var CryptoJS = CryptoJS || function(y, h) {
    var j = {}
      , g = j.lib = {}
      , f = function() {}
      , z = g.Base = {
        extend: function(b) {
            f.prototype = this;
            var d = new f;
            b && d.mixIn(b);
            d.hasOwnProperty("init") || (d.init = function() {
                d.$super.init.apply(this, arguments)
            }
            );
            d.init.prototype = d;
            d.$super = this;
            return d
        },
        create: function() {
            var b = this.extend();
            b.init.apply(b, arguments);
            return b
        },
        init: function() {},
        mixIn: function(b) {
            for (var d in b) {
                b.hasOwnProperty(d) && (this[d] = b[d])
            }
            b.hasOwnProperty("toString") && (this.toString = b.toString)
        },
        clone: function() {
            return this.init.prototype.extend(this)
        }
    }
      , c = g.WordArray = z.extend({
        init: function(b, d) {
            b = this.words = b || [];
            this.sigBytes = d != h ? d : 4 * b.length
        },
        toString: function(b) {
            return (b || t).stringify(this)
        },
        concat: function(d) {
            var n = this.words
              , b = d.words
              , l = this.sigBytes;
            d = d.sigBytes;
            this.clamp();
            if (l % 4) {
                for (var e = 0; e < d; e++) {
                    n[l + e >>> 2] |= (b[e >>> 2] >>> 24 - 8 * (e % 4) & 255) << 24 - 8 * ((l + e) % 4)
                }
            } else {
                if (65535 < b.length) {
                    for (e = 0; e < d; e += 4) {
                        n[l + e >>> 2] = b[e >>> 2]
                    }
                } else {
                    n.push.apply(n, b)
                }
            }
            this.sigBytes += d;
            return this
        },
        clamp: function() {
            var b = this.words
              , d = this.sigBytes;
            b[d >>> 2] &= 4294967295 << 32 - 8 * (d % 4);
            b.length = y.ceil(d / 4)
        },
        clone: function() {
            var b = z.clone.call(this);
            b.words = this.words.slice(0);
            return b
        },
        random: function(d) {
            for (var e = [], b = 0; b < d; b += 4) {
                e.push(4294967296 * y.random() | 0)
            }
            return new c.init(e,d)
        }
    })
      , o = j.enc = {}
      , t = o.Hex = {
        stringify: function(d) {
            var n = d.words;
            d = d.sigBytes;
            for (var b = [], l = 0; l < d; l++) {
                var e = n[l >>> 2] >>> 24 - 8 * (l % 4) & 255;
                b.push((e >>> 4).toString(16));
                b.push((e & 15).toString(16))
            }
            return b.join("")
        },
        parse: function(d) {
            for (var l = d.length, b = [], e = 0; e < l; e += 2) {
                b[e >>> 3] |= parseInt(d.substr(e, 2), 16) << 24 - 4 * (e % 8)
            }
            return new c.init(b,l / 2)
        }
    }
      , k = o.Latin1 = {
        stringify: function(d) {
            var l = d.words;
            d = d.sigBytes;
            for (var b = [], e = 0; e < d; e++) {
                b.push(String.fromCharCode(l[e >>> 2] >>> 24 - 8 * (e % 4) & 255))
            }
            return b.join("")
        },
        parse: function(d) {
            for (var l = d.length, b = [], e = 0; e < l; e++) {
                b[e >>> 2] |= (d.charCodeAt(e) & 255) << 24 - 8 * (e % 4)
            }
            return new c.init(b,l)
        }
    }
      , m = o.Utf8 = {
        stringify: function(b) {
            try {
                return decodeURIComponent(escape(k.stringify(b)))
            } catch (d) {
                throw Error("Malformed UTF-8 data")
            }
        },
        parse: function(b) {
            return k.parse(unescape(encodeURIComponent(b)))
        }
    }
      , a = g.BufferedBlockAlgorithm = z.extend({
        reset: function() {
            this._data = new c.init;
            this._nDataBytes = 0
        },
        _append: function(b) {
            "string" == typeof b && (b = m.parse(b));
            this._data.concat(b);
            this._nDataBytes += b.sigBytes
        },
        _process: function(n) {
            var s = this._data
              , l = s.words
              , q = s.sigBytes
              , p = this.blockSize
              , d = q / (4 * p)
              , d = n ? y.ceil(d) : y.max((d | 0) - this._minBufferSize, 0);
            n = d * p;
            q = y.min(4 * n, q);
            if (n) {
                for (var r = 0; r < n; r += p) {
                    this._doProcessBlock(l, r)
                }
                r = l.splice(0, n);
                s.sigBytes -= q
            }
            return new c.init(r,q)
        },
        clone: function() {
            var b = z.clone.call(this);
            b._data = this._data.clone();
            return b
        },
        _minBufferSize: 0
    });
    g.Hasher = a.extend({
        cfg: z.extend(),
        init: function(b) {
            this.cfg = this.cfg.extend(b);
            this.reset()
        },
        reset: function() {
            a.reset.call(this);
            this._doReset()
        },
        update: function(b) {
            this._append(b);
            this._process();
            return this
        },
        finalize: function(b) {
            b && this._append(b);
            return this._doFinalize()
        },
        blockSize: 16,
        _createHelper: function(b) {
            return function(e, d) {
                return (new b.init(d)).finalize(e)
            }
        },
        _createHmacHelper: function(b) {
            return function(e, d) {
                return (new i.HMAC.init(b,d)).finalize(e)
            }
        }
    });
    var i = j.algo = {};
    return j
}



var DES3 = {
    iv: function() {
        return $.WebSite.formatDate(new Date(), "yyyyMMdd")
    },
    encrypt: function(b, c, a) {
        if (c) {
            return (CryptoJS.TripleDES.encrypt(b, CryptoJS.enc.Utf8.parse(c), {
                iv: CryptoJS.enc.Utf8.parse(a || DES3.iv()),
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            })).toString()
        }
        return ""
    },
    decrypt: function(b, c, a) {
        if (c) {
            return CryptoJS.enc.Utf8.stringify(CryptoJS.TripleDES.decrypt(b, CryptoJS.enc.Utf8.parse(c), {
                iv: CryptoJS.enc.Utf8.parse(a || DES3.iv()),
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            })).toString()
        }
        return ""
    }
};








// d: "j69EnGTHzi9ooPCpCFzTIKhc"
// b = [1781938501, 1850168392, 2053716335, 1867531120, 1128692308, 1229678691]