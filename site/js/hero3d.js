/* Potros hero: dependency-free WebGL scene (dusk backyard: pergola, kitchen, fire pit, pavers).
   Exposes window.PotrosHero.init(canvas) -> { setProgress(p), setPointer(x,y), destroy() } or null if WebGL is unavailable. */
(function () {
  'use strict';

  /* ---------- tiny math ---------- */
  var M = {
    persp: function (fovy, asp, n, f) {
      var t = 1 / Math.tan(fovy / 2), r = 1 / (n - f);
      return new Float32Array([t / asp, 0, 0, 0, 0, t, 0, 0, 0, 0, (f + n) * r, -1, 0, 0, 2 * f * n * r, 0]);
    },
    look: function (e, c, up) {
      var zx = e[0] - c[0], zy = e[1] - c[1], zz = e[2] - c[2], l = Math.hypot(zx, zy, zz); zx /= l; zy /= l; zz /= l;
      var xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx; l = Math.hypot(xx, xy, xz); xx /= l; xy /= l; xz /= l;
      var yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
      return new Float32Array([xx, yx, zx, 0, xy, yy, zy, 0, xz, yz, zz, 0, -(xx * e[0] + xy * e[1] + xz * e[2]), -(yx * e[0] + yy * e[1] + yz * e[2]), -(zx * e[0] + zy * e[1] + zz * e[2]), 1]);
    },
    mul: function (a, b) {
      var o = new Float32Array(16);
      for (var i = 0; i < 4; i++) for (var j = 0; j < 4; j++) o[j * 4 + i] = a[i] * b[j * 4] + a[4 + i] * b[j * 4 + 1] + a[8 + i] * b[j * 4 + 2] + a[12 + i] * b[j * 4 + 3];
      return o;
    }
  };
  var lerp = function (a, b, t) { return a + (b - a) * t; };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var smooth = function (t) { return t * t * (3 - 2 * t); };
  var seed = 7; var rnd = function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

  /* ---------- geometry builder (non-indexed, per-vertex color + emissive) ---------- */
  function Geo() { this.p = []; this.n = []; this.c = []; this.e = []; }
  Geo.prototype.tri = function (a, b, c, n, col, em) {
    var s = [a, b, c];
    for (var i = 0; i < 3; i++) { this.p.push(s[i][0], s[i][1], s[i][2]); this.n.push(n[0], n[1], n[2]); this.c.push(col[0], col[1], col[2]); this.e.push(em); }
  };
  Geo.prototype.quad = function (a, b, c, d, n, col, em) { this.tri(a, b, c, n, col, em); this.tri(a, c, d, n, col, em); };
  Geo.prototype.box = function (cx, cy, cz, sx, sy, sz, col, em, ry, skipBottom) {
    em = em || 0; ry = ry || 0;
    var hx = sx / 2, hy = sy / 2, hz = sz / 2, cs = Math.cos(ry), sn = Math.sin(ry);
    var T = function (x, y, z) { return [cx + x * cs + z * sn, cy + y, cz - x * sn + z * cs]; };
    var N = function (x, y, z) { return [x * cs + z * sn, y, -x * sn + z * cs]; };
    var v = [T(-hx, -hy, -hz), T(hx, -hy, -hz), T(hx, hy, -hz), T(-hx, hy, -hz), T(-hx, -hy, hz), T(hx, -hy, hz), T(hx, hy, hz), T(-hx, hy, hz)];
    var shade = function (k) { return [col[0] * k, col[1] * k, col[2] * k]; };
    this.quad(v[4], v[5], v[6], v[7], N(0, 0, 1), shade(.92), em);
    this.quad(v[1], v[0], v[3], v[2], N(0, 0, -1), shade(.92), em);
    this.quad(v[5], v[1], v[2], v[6], N(1, 0, 0), shade(.85), em);
    this.quad(v[0], v[4], v[7], v[3], N(-1, 0, 0), shade(.85), em);
    this.quad(v[7], v[6], v[2], v[3], N(0, 1, 0), col, em);
    if (!skipBottom) this.quad(v[0], v[1], v[5], v[4], N(0, -1, 0), shade(.6), em);
  };
  Geo.prototype.cyl = function (cx, cy, cz, r, h, seg, col, em, rTop) {
    em = em || 0; rTop = rTop === undefined ? r : rTop;
    for (var i = 0; i < seg; i++) {
      var a0 = i / seg * 6.2832, a1 = (i + 1) / seg * 6.2832, am = (a0 + a1) / 2;
      var n = [Math.cos(am), 0, Math.sin(am)];
      var k = .78 + .22 * Math.cos(am - 2.2);
      var cc = [col[0] * k, col[1] * k, col[2] * k];
      var p0 = [cx + Math.cos(a0) * r, cy, cz + Math.sin(a0) * r], p1 = [cx + Math.cos(a1) * r, cy, cz + Math.sin(a1) * r];
      var q0 = [cx + Math.cos(a0) * rTop, cy + h, cz + Math.sin(a0) * rTop], q1 = [cx + Math.cos(a1) * rTop, cy + h, cz + Math.sin(a1) * rTop];
      this.quad(p0, p1, q1, q0, n, cc, em);
      this.tri([cx, cy + h, cz], q0, q1, [0, 1, 0], col, em);
    }
  };
  Geo.prototype.top = function (x0, z0, x1, z1, y, col, em) { this.quad([x0, y, z1], [x1, y, z1], [x1, y, z0], [x0, y, z0], [0, 1, 0], col, em || 0); };

  /* ---------- scene content ---------- */
  var STONE = [.34, .31, .29], STONE_D = [.22, .2, .19], DARK = [.1, .095, .09], WOOD = [.2, .13, .09], PAV = [.40, .37, .34];
  var FIRE = [0, .0, 3.2]; // fire pit center

  function buildScene() {
    var g = new Geo(), i, j, x, z, k;
    // ground (lawn) + terrace
    g.top(-60, -40, 60, 40, -.04, [.045, .075, .05]);
    // pavers in running bond: terrace x[-9,9] z[-6.5,8]
    for (z = -6.5; z < 8; z += .5) {
      var row = Math.round((z + 6.5) / .5), off = (row % 2) * .5;
      for (x = -9 + off; x < 9; x += 1) {
        var v = .82 + rnd() * .3, w = [PAV[0] * v, PAV[1] * v, PAV[2] * v * (.95 + rnd() * .1)];
        g.top(x + .02, z + .02, x + .98, z + .48, 0, w);
      }
    }
    // stamped-concrete band around fire pit (darker ring of tiles)
    // house backdrop
    g.box(0, 3.6, -11, 34, 8, 4, [.075, .07, .07]);
    g.box(0, 8.6, -11, 36, .5, 4.6, [.05, .045, .045]);
    for (i = -6; i <= 6; i++) { // lit windows
      if (Math.abs(i) < 2) continue;
      g.box(i * 2.4, 3.4, -8.95, 1.5, 2.4, .1, [1, .7, .38], 1.15);
      g.box(i * 2.4, 3.4, -8.9, 1.62, 2.52, .08, DARK);
    }
    // stone fireplace / TV wall
    g.box(0, 2.1, -6.1, 5.2, 4.2, .9, STONE_D);
    for (j = 0; j < 14; j++) for (k = 0; k < 6; k++) { var vv = .8 + rnd() * .4; g.box(-2.3 + k * .9 + (j % 2) * .22, .15 + j * .3, -5.62, .84, .26, .1, [STONE[0] * vv, STONE[1] * vv, STONE[2] * vv]); }
    g.box(0, .75, -5.55, 1.7, 1.1, .12, [1, .5, .2], 1.6); // fireplace glow
    g.box(0, 1.5, -5.5, 2.2, .14, .3, DARK);
    g.box(0, 2.95, -5.52, 2.6, 1.3, .08, [.02, .02, .03], .0); // tv

    // pergola: columns + beams + rafters
    var cols = [[-7, -5.2], [-3.5, -5.2], [0, -5.2], [3.5, -5.2], [7, -5.2], [-7, -1.4], [-3.5, -1.4], [0, -1.4], [3.5, -1.4], [7, -1.4], [-7, 2.0]];
    var H = 3.5, c;
    for (i = 0; i < cols.length; i++) {
      c = cols[i];
      g.box(c[0], .35, c[1], .95, .7, .95, STONE_D);
      g.box(c[0], H / 2 + .35, c[1], .62, H - .1, .62, [.9, .88, .84].map(function (t) { return t * .17; }));
      g.box(c[0], H + .12, c[1], .86, .16, .86, STONE_D);
    }
    for (j = 0; j < 2; j++) { z = [-5.2, -1.4][j]; g.box(0, H + .38, z, 15.2, .36, .3, WOOD); }
    for (x = -7.2; x <= 7.2; x += .55) g.box(x, H + .64, -3.3, .12, .2, 4.8 + 1.4, WOOD);
    for (x = -7; x <= 7; x += 1.75) g.box(x, H + .78, -3.3, .06, .08, 6.6, WOOD);
    // string lights under beams (emissive dots)
    for (i = 0; i < 28; i++) g.box(-7 + i * .52, H - .1 - Math.sin(i * .5) * .08, -1.4, .09, .09, .09, [1, .78, .45], 3.2);

    // kitchen island + stool bar (36 ft total across)
    g.box(0, .5, -3.7, 12, 1, 1.1, [.07, .065, .06]);
    g.box(0, 1.04, -3.7, 12.3, .1, 1.5, [.55, .5, .46]);
    g.box(0, .96, -3.0, 12, .04, .04, [1, .6, .3], 2.4);
    g.box(0, 1.0, -4.4, 4.2, .75, .7, [.12, .11, .1]); // grill
    g.box(0, 1.46, -4.4, 4.2, .08, .7, [.3, .3, .3]);
    for (i = -4; i <= 4; i++) { g.cyl(i * 1.28, 0, -2.35, .22, .6, 12, [.1, .08, .07]); g.cyl(i * 1.28, .6, -2.35, .26, .08, 12, [.35, .15, .12]); }
    // sofas / lounge
    g.box(-5.2, .35, 2.4, 3.2, .7, 1.1, [.16, .15, .14], 0, .35); g.box(-5.2, .8, 1.95, 3.2, .7, .3, [.14, .13, .12], 0, .35);
    g.box(5.2, .35, 2.4, 3.2, .7, 1.1, [.16, .15, .14], 0, -.35); g.box(5.2, .8, 1.95, 3.2, .7, .3, [.14, .13, .12], 0, -.35);
    g.box(-5.2, .12, 2.9, 1.4, .12, 1.0, [.5, .12, .13], 0, .35);

    // sunken fire pit with seating wall ring
    for (i = 0; i < 40; i++) {
      var a = i / 40 * 6.2832, ca = Math.cos(a), sa = Math.sin(a), vq = .85 + rnd() * .3;
      g.box(FIRE[0] + ca * 2.9, .27, FIRE[2] + sa * 2.9, .78, .54, 1.5, [STONE[0] * vq, STONE[1] * vq, STONE[2] * vq], 0, -a);
      g.box(FIRE[0] + ca * 2.9, .58, FIRE[2] + sa * 2.9, .86, .1, 1.6, [.5 * vq, .47 * vq, .44 * vq], 0, -a);
    }
    g.cyl(FIRE[0], .02, FIRE[2], 1.05, .5, 24, [.12, .11, .1]);
    g.cyl(FIRE[0], .5, FIRE[2], .86, .04, 24, [.45, .13, .05], .55);
    for (i = 0; i < 10; i++) { var aa = i / 10 * 6.2832; g.box(FIRE[0] + Math.cos(aa) * .25, .62, FIRE[2] + Math.sin(aa) * .25, .12, .12, .5, [.12, .06, .04], 0, aa); }

    // retaining walls (stacked block courses) with step
    for (j = 0; j < 2; j++) for (x = -10; x < 10; x += 1.2) {
      var vw = .8 + rnd() * .35;
      g.box(x + (j % 2) * .6, .22 + j * .42, 9.4 + j * .0, 1.14, .4, .7, [STONE[0] * vw, STONE[1] * vw, STONE[2] * vw]);
    }
    for (j = 0; j < 3; j++) for (z = -6; z < 9; z += 1.2) {
      var vw2 = .8 + rnd() * .35;
      g.box(-10.3, .22 + j * .42, z + (j % 2) * .6, .7, .4, 1.14, [STONE[0] * vw2, STONE[1] * vw2, STONE[2] * vw2]);
      g.box(10.3, .22 + j * .42, z + (j % 2) * .6, .7, .4, 1.14, [STONE[0] * vw2, STONE[1] * vw2, STONE[2] * vw2]);
    }
    // path lights
    for (i = 0; i < 8; i++) { var pz = 4.8 + i * .0; g.box(-9.2 + i * 2.6, .35, 8.4, .14, .7, .14, [.08, .08, .08]); g.box(-9.2 + i * 2.6, .74, 8.4, .2, .1, .2, [1, .72, .4], 3); }

    // landscaping: trees + shrubs
    for (i = 0; i < 26; i++) {
      var tx = (rnd() - .5) * 56, tz = -14 + rnd() * -10 - (i % 2) * 6;
      if (rnd() > .45) tz = 13 + rnd() * 8;
      var th = 4 + rnd() * 5, tr = 1.4 + rnd() * 1.4, gc = [.03 + rnd() * .03, .09 + rnd() * .05, .05 + rnd() * .03];
      g.cyl(tx, 0, tz, .22, th * .4, 6, [.08, .05, .035]);
      g.cyl(tx, th * .3, tz, tr, th * .8, 7, gc, 0, .05);
    }
    for (i = 0; i < 30; i++) {
      var bx = -9 + rnd() * 18, bz = 9.9 + rnd() * 1.4;
      g.cyl(bx, 0, bz, .45 + rnd() * .4, .6 + rnd() * .5, 7, [.04, .1 + rnd() * .05, .06], 0, .1);
    }
    return g;
  }

  /* ---------- shaders ---------- */
  var VS = 'attribute vec3 aP;attribute vec3 aN;attribute vec3 aC;attribute float aE;uniform mat4 uVP;varying vec3 vP;varying vec3 vN;varying vec3 vC;varying float vE;void main(){vP=aP;vN=aN;vC=aC;vE=aE;gl_Position=uVP*vec4(aP,1.0);}';
  var FS = 'precision mediump float;varying vec3 vP;varying vec3 vN;varying vec3 vC;varying float vE;uniform vec3 uCam;uniform vec3 uFire;uniform float uFl;uniform float uT;\n' +
    'vec3 pl(vec3 lp,vec3 col,float k,vec3 n){vec3 d=lp-vP;float l=length(d);float nd=max(dot(n,d/l)*.6+.4,0.);return col*nd*k/(1.+l*l*.045);}\n' +
    'void main(){vec3 n=normalize(vN);' +
    'vec3 amb=vec3(.20,.24,.36)*(.55+.45*n.y);' +
    'vec3 moon=vec3(.22,.28,.45)*max(dot(n,normalize(vec3(-.4,.8,.5))),0.)*.8;' +
    'vec3 L=amb+moon;' +
    'L+=pl(uFire+vec3(0.,.9,0.),vec3(1.,.42,.14),1.9*uFl,n);' +
    'L+=pl(vec3(-4.,3.1,-1.4),vec3(1.,.66,.34),1.5,n)+pl(vec3(4.,3.1,-1.4),vec3(1.,.66,.34),1.5,n)+pl(vec3(0.,3.1,-3.),vec3(1.,.66,.34),1.4,n);' +
    'L+=pl(vec3(0.,1.2,-5.2),vec3(1.,.5,.2),1.3,n);' +
    'vec3 col=vC*L+vC*vE*.0;col+=vC*max(vE-.0,0.)*1.0;' +
    'float h=clamp(vP.y*.35,0.,1.);col*=.78+.22*h;' +
    'float d=length(vP-uCam);float fog=1.-exp(-d*d*.0011);vec3 fc=mix(vec3(.05,.06,.11),vec3(.16,.09,.11),smoothstep(0.,14.,15.-vP.y*.4));col=mix(col,fc,clamp(fog,0.,1.));' +
    'col=pow(col,vec3(.9));gl_FragColor=vec4(col,1.);}';
  var SKY_VS = 'attribute vec2 aP;varying vec2 vUv;void main(){vUv=aP;gl_Position=vec4(aP,.9999,1.);}';
  var SKY_FS = 'precision mediump float;varying vec2 vUv;uniform float uAsp;uniform float uYaw;uniform float uPitch;uniform float uT;\n' +
    'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}\n' +
    'void main(){vec2 uv=vUv;float y=uv.y*.5+.5;' +
    'vec3 top=vec3(.015,.02,.055),mid=vec3(.07,.07,.15),hor=vec3(.34,.12,.12);' +
    'vec3 c=mix(hor,mid,smoothstep(.35,.62,y));c=mix(c,top,smoothstep(.6,1.,y));' +
    'vec2 sp=vec2(uv.x*uAsp+uYaw*2.2,uv.y+uPitch*1.5)*vec2(90.,60.);vec2 id=floor(sp);float s=step(.985,h(id));float tw=.6+.4*sin(uT*2.+h(id)*40.);' +
    'c+=s*tw*smoothstep(.45,.8,y)*vec3(.9,.9,1.)*(1.-length(fract(sp)-.5)*1.6);' +
    'c+=vec3(.5,.2,.12)*exp(-pow((y-.4)*5.,2.))*.35;gl_FragColor=vec4(c,1.);}';
  var PS_VS = 'attribute vec4 aS;uniform mat4 uVP;uniform float uT;uniform vec3 uFire;uniform float uH;uniform float uPx;varying float vA;varying float vK;varying float vM;\n' +
    'float f(float x){return fract(sin(x*91.345)*47453.5453);}\n' +
    'void main(){float s=aS.x;float kind=aS.y;vec3 p;float size;float life;' +
    'if(kind<.5){life=fract(uT*.9+s);float r=(1.-life)*.55*f(s+1.);float a=f(s+2.)*6.2832;' +
    'p=uFire+vec3(cos(a)*r+sin(uT*3.+s*40.)*.06*life,.55+life*1.7,sin(a)*r);size=(1.-life)*1.0+.15;vA=(1.-life)*(1.-life);vK=life;vM=0.;}' +
    'else if(kind<1.5){life=fract(uT*.18+s);float a=f(s+3.)*6.2832;float r=.2+f(s+4.)*.9;' +
    'p=uFire+vec3(cos(a)*r+sin(uT*.8+s*30.)*.9*life,.9+life*6.,sin(a)*r+cos(uT*.7+s*20.)*.9*life);size=(1.-life)*.18+.05;vA=sin(life*3.1416);vK=.2;vM=1.;}' +
    'else{float a=f(s+5.)*6.2832;float r=3.+f(s+6.)*16.;p=vec3(cos(a)*r,.5+f(s+7.)*3.5+sin(uT*.6+s*50.)*.4,sin(a)*r*.7+2.)+vec3(sin(uT*.3+s*20.)*.8,0.,cos(uT*.25+s*17.)*.8);size=.1;vA=.5+.5*sin(uT*1.7+s*60.);vK=.3;vM=2.;}' +
    'vec4 cp=uVP*vec4(p,1.);gl_Position=cp;gl_PointSize=clamp(size*uPx/cp.w*(kind<.5?2.7:2.4),1.,160.);}';
  var PS_FS = 'precision mediump float;varying float vA;varying float vK;varying float vM;void main(){vec2 d=gl_PointCoord-.5;float r=length(d)*2.;if(r>1.)discard;float a=pow(1.-r,2.)*vA;' +
    'vec3 hot=vec3(1.,.82,.4),mid=vec3(1.,.32,.08),cool=vec3(.5,.05,.04);vec3 c=mix(hot,mid,smoothstep(0.,.35,vK));c=mix(c,cool,smoothstep(.35,1.,vK));' +
    'if(vM>1.5)c=vec3(.7,1.,.5);else if(vM>.5)c=vec3(1.,.55,.2);gl_FragColor=vec4(c*a*1.05,a);}';

  function sh(gl, type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); } return s; }
  function prog(gl, vs, fs) { var p = gl.createProgram(); gl.attachShader(p, sh(gl, gl.VERTEX_SHADER, vs)); gl.attachShader(p, sh(gl, gl.FRAGMENT_SHADER, fs)); gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p)); return p; }

  /* ---------- camera path (pos, target) ---------- */
  var PATH = [
    { p: [-8.8, 3.5, 12.8], t: [0, 1.2, -1.5], f: 52 },
    { p: [-6.0, 2.4, 10.8], t: [0, 1.5, -1.5], f: 54 },
    { p: [-2.4, 1.55, 8.0], t: [0, 1.5, 0.0], f: 58 },
    { p: [1.8, 1.35, 5.8], t: [0.5, 1.9, -3.0], f: 62 },
    { p: [0.0, 1.55, 1.2], t: [0, 2.3, -5.2], f: 66 },
    { p: [0.0, 1.7, -1.2], t: [0, 2.4, -6.0], f: 70 }
  ];
  function camAt(u) {
    var n = PATH.length - 1, x = clamp(u, 0, 1) * n, i = Math.min(Math.floor(x), n - 1), f = smooth(x - i), a = PATH[i], b = PATH[i + 1];
    return { p: [lerp(a.p[0], b.p[0], f), lerp(a.p[1], b.p[1], f), lerp(a.p[2], b.p[2], f)], t: [lerp(a.t[0], b.t[0], f), lerp(a.t[1], b.t[1], f), lerp(a.t[2], b.t[2], f)], f: lerp(a.f, b.f, f) };
  }

  function init(canvas, opts) {
    opts = opts || {};
    var gl = canvas.getContext('webgl', { antialias: true, alpha: false, powerPreference: 'high-performance' }) || canvas.getContext('experimental-webgl');
    if (!gl) return null;
    var main, sky, ps;
    try { main = prog(gl, VS, FS); sky = prog(gl, SKY_VS, SKY_FS); ps = prog(gl, PS_VS, PS_FS); } catch (e) { if (window.console) console.warn('[hero3d]', e.message); return null; }

    var geo = buildScene(), count = geo.p.length / 3;
    var mk = function (arr) { var b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(arr), gl.STATIC_DRAW); return b; };
    var bufs = { p: mk(geo.p), n: mk(geo.n), c: mk(geo.c), e: mk(geo.e) };
    var skyBuf = mk([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]);
    var parts = [], NF = 520, NE = 140, NG = 70, i;
    for (i = 0; i < NF; i++) parts.push(rnd(), 0, 0, 0);
    for (i = 0; i < NE; i++) parts.push(rnd(), 1, 0, 0);
    for (i = 0; i < NG; i++) parts.push(rnd(), 2, 0, 0);
    var partBuf = mk(parts), partCount = NF + NE + NG;

    var loc = function (p, n) { return gl.getUniformLocation(p, n); }, att = function (p, n) { return gl.getAttribLocation(p, n); };
    var U = { vp: loc(main, 'uVP'), cam: loc(main, 'uCam'), fire: loc(main, 'uFire'), fl: loc(main, 'uFl'), t: loc(main, 'uT') };
    var A = { p: att(main, 'aP'), n: att(main, 'aN'), c: att(main, 'aC'), e: att(main, 'aE') };
    var SU = { asp: loc(sky, 'uAsp'), yaw: loc(sky, 'uYaw'), pitch: loc(sky, 'uPitch'), t: loc(sky, 'uT') }, SA = att(sky, 'aP');
    var PU = { vp: loc(ps, 'uVP'), t: loc(ps, 'uT'), fire: loc(ps, 'uFire'), px: loc(ps, 'uPx') }, PA = att(ps, 'aS');

    var prog_ = 0, progT = 0, mx = 0, my = 0, tx = 0, ty = 0, raf = 0, start = performance.now(), w = 0, h = 0, running = true, staticMode = !!opts.static, lastW = 0;
    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.6), cw = canvas.clientWidth, ch = canvas.clientHeight;
      if (!cw || !ch) return; w = Math.round(cw * dpr); h = Math.round(ch * dpr);
      if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
      gl.viewport(0, 0, w, h);
    }
    function frame(now) {
      var t = (now - start) / 1000;
      progT += (prog_ - progT) * .075; mx += (tx - mx) * .05; my += (ty - my) * .05;
      var cam = camAt(progT), drift = staticMode ? 0 : 1;
      var idle = 1 - smooth(clamp(progT * 3, 0, 1)) * .6;
      var px = cam.p[0] + (Math.sin(t * .18) * .8 + mx * .9) * idle * drift, py = cam.p[1] + (Math.sin(t * .23) * .12 - my * .25) * idle * drift, pz = cam.p[2] + Math.cos(t * .15) * .6 * idle * drift;
      var eye = [px, py, pz], tgt = [cam.t[0] + mx * .9, cam.t[1] - my * .35, cam.t[2]];
      var asp = w / h, fov = (cam.f + (asp < 1 ? 14 : 0)) * Math.PI / 180;
      var vp = M.mul(M.persp(fov, asp, .1, 140), M.look(eye, tgt, [0, 1, 0]));
      var fl = .86 + Math.sin(t * 9.1) * .07 + Math.sin(t * 13.7 + 1.3) * .06 + Math.sin(t * 5.3) * .05;
      var yaw = Math.atan2(tgt[0] - eye[0], -(tgt[2] - eye[2])), pitch = Math.atan2(tgt[1] - eye[1], 10);

      gl.clearColor(.03, .03, .06, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      // sky
      gl.disable(gl.DEPTH_TEST); gl.disable(gl.BLEND); gl.useProgram(sky);
      gl.bindBuffer(gl.ARRAY_BUFFER, skyBuf); gl.enableVertexAttribArray(SA); gl.vertexAttribPointer(SA, 2, gl.FLOAT, false, 0, 0);
      gl.uniform1f(SU.asp, asp); gl.uniform1f(SU.yaw, yaw); gl.uniform1f(SU.pitch, pitch); gl.uniform1f(SU.t, t);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      // scene
      gl.enable(gl.DEPTH_TEST); gl.useProgram(main);
      var bind = function (a, b, n) { gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.enableVertexAttribArray(a); gl.vertexAttribPointer(a, n, gl.FLOAT, false, 0, 0); };
      bind(A.p, bufs.p, 3); bind(A.n, bufs.n, 3); bind(A.c, bufs.c, 3); bind(A.e, bufs.e, 1);
      gl.uniformMatrix4fv(U.vp, false, vp); gl.uniform3f(U.cam, eye[0], eye[1], eye[2]); gl.uniform3f(U.fire, FIRE[0], FIRE[1], FIRE[2]); gl.uniform1f(U.fl, fl); gl.uniform1f(U.t, t);
      gl.drawArrays(gl.TRIANGLES, 0, count);
      gl.disableVertexAttribArray(A.n); gl.disableVertexAttribArray(A.c); gl.disableVertexAttribArray(A.e);
      // particles (additive)
      gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE); gl.depthMask(false);
      gl.useProgram(ps); gl.bindBuffer(gl.ARRAY_BUFFER, partBuf); gl.enableVertexAttribArray(PA); gl.vertexAttribPointer(PA, 4, gl.FLOAT, false, 0, 0);
      gl.uniformMatrix4fv(PU.vp, false, vp); gl.uniform1f(PU.t, staticMode ? 3.7 : t); gl.uniform3f(PU.fire, FIRE[0], FIRE[1], FIRE[2]); gl.uniform1f(PU.px, h * .5 / Math.tan(fov / 2) * .12);
      gl.drawArrays(gl.POINTS, 0, partCount);
      gl.depthMask(true); gl.disable(gl.BLEND); gl.disableVertexAttribArray(A.p);
      if (running && !staticMode) raf = requestAnimationFrame(frame);
    }
    resize();
    var onResize = function () { resize(); if (staticMode) frame(performance.now()); };
    window.addEventListener('resize', onResize);
    var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function (en) {
      var vis = en[0].isIntersecting;
      if (vis && !running && !staticMode) { running = true; raf = requestAnimationFrame(frame); }
      if (!vis) { running = false; cancelAnimationFrame(raf); }
    }) : null;
    if (io) io.observe(canvas);
    raf = requestAnimationFrame(frame);

    return {
      setProgress: function (p) { prog_ = clamp(p, 0, 1); if (staticMode) { progT = prog_; frame(performance.now()); } },
      jump: function (p) { prog_ = progT = clamp(p, 0, 1); },
      setPointer: function (x, y) { tx = x; ty = y; },
      destroy: function () { running = false; cancelAnimationFrame(raf); window.removeEventListener('resize', onResize); if (io) io.disconnect(); }
    };
  }
  window.PotrosHero = { init: init };
})();
