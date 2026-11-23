import {
  $,
  n
} from "./chunk-RZBBS6KD.js";

// node_modules/preact/jsx-runtime/dist/jsxRuntime.mjs
var e = /["&<]/;
function n2(r) {
  if (!r.length || !e.test(r)) return r;
  for (var t = 0, n3 = 0, f2 = "", o2 = ""; n3 < r.length; n3++) {
    switch (r.charCodeAt(n3)) {
      case 34:
        o2 = "&quot;";
        break;
      case 38:
        o2 = "&amp;";
        break;
      case 60:
        o2 = "&lt;";
        break;
      default:
        continue;
    }
    n3 != t && (f2 += r.slice(t, n3)), f2 += o2, t = n3 + 1;
  }
  return n3 != t && (f2 += r.slice(t, n3)), f2;
}
var f = Symbol.for("pv");
var o = 0;
var u = Array.isArray;
function a(t, e2, n3, u2, a2, i2) {
  e2 || (e2 = {});
  var c2, l2, p2 = e2;
  if ("ref" in p2 && "function" != typeof t) for (l2 in p2 = {}, e2) "ref" == l2 ? c2 = e2[l2] : p2[l2] = e2[l2];
  var s2 = { type: t, props: p2, key: n3, ref: c2, __k: null, __: null, __b: 0, __e: null, __c: null, constructor: f, __v: --o, __i: -1, __u: 0 };
  return (a2 || i2) && (s2.__source = a2, s2.__self = i2), n.vnode && n.vnode(s2), s2;
}
function i(r) {
  var e2 = a($, { tpl: r, exprs: [].slice.call(arguments, 1) });
  return e2.key = e2.__v, e2;
}
var c = {};
var l = /[A-Z]/g;
function p(t, e2) {
  if (n.attr) {
    var f2 = n.attr(t, e2);
    if ("string" == typeof f2) return f2;
  }
  if (e2 = (function(r) {
    return null != r && "object" == typeof r && "function" == typeof r.valueOf ? r.valueOf() : r;
  })(e2), "ref" == t || "key" == t) return "";
  if ("style" == t && "object" == typeof e2) {
    var o2 = "";
    for (var u2 in e2) {
      var a2 = e2[u2];
      null != a2 && "" !== a2 && (o2 = o2 + ("-" == u2[0] ? u2 : c[u2] || (c[u2] = u2.replace(l, "-$&").toLowerCase())) + ":" + a2 + ";");
    }
    return t + '="' + n2(o2) + '"';
  }
  return null == e2 || false === e2 || "function" == typeof e2 || "object" == typeof e2 ? "" : true === e2 ? t : t + '="' + n2("" + e2) + '"';
}
function s(r) {
  if (null == r || "boolean" == typeof r || "function" == typeof r) return null;
  if ("object" == typeof r) {
    if (r.constructor === f) return r;
    if (u(r)) {
      for (var t = 0; t < r.length; t++) r[t] = s(r[t]);
      return r;
    }
  }
  return n2("" + r);
}
export {
  $ as Fragment,
  a as jsx,
  p as jsxAttr,
  a as jsxDEV,
  s as jsxEscape,
  i as jsxTemplate,
  a as jsxs
};
//# sourceMappingURL=preact_jsx-dev-runtime.js.map
