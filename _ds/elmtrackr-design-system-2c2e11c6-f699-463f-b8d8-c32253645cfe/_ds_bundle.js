/* @ds-bundle: {"format":3,"namespace":"ElmtrackrDesignSystem_2c2e11","components":[{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Card","sourcePath":"components/core/Card.jsx"},{"name":"Eyebrow","sourcePath":"components/core/Eyebrow.jsx"},{"name":"ProgressRing","sourcePath":"components/data/ProgressRing.jsx"},{"name":"SegmentedBar","sourcePath":"components/data/SegmentedBar.jsx"},{"name":"StatCard","sourcePath":"components/data/StatCard.jsx"},{"name":"EmptyState","sourcePath":"components/feedback/EmptyState.jsx"},{"name":"Toast","sourcePath":"components/feedback/Toast.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"},{"name":"Segmented","sourcePath":"components/forms/Segmented.jsx"},{"name":"BottomNav","sourcePath":"components/navigation/BottomNav.jsx"}],"sourceHashes":{"components/core/Badge.jsx":"57168493c1cd","components/core/Button.jsx":"ba7a2c131f7d","components/core/Card.jsx":"59b14b016637","components/core/Eyebrow.jsx":"f45e94171a4f","components/data/ProgressRing.jsx":"d84801542f13","components/data/SegmentedBar.jsx":"938013e7aa44","components/data/StatCard.jsx":"85512a252ec0","components/feedback/EmptyState.jsx":"8f1b1a228c3f","components/feedback/Toast.jsx":"e7b10e56cdb3","components/forms/Input.jsx":"a45bdb8a4d5d","components/forms/Segmented.jsx":"0277a93fc95e","components/navigation/BottomNav.jsx":"cb9d184d354b","ui_kits/mobile-app/HomeScreen.jsx":"ea8dc775ead8","ui_kits/mobile-app/ReportsScreen.jsx":"812b846cbe38","ui_kits/mobile-app/SettingsScreen.jsx":"edea81506c74","ui_kits/mobile-app/ShiftRow.jsx":"81a457f53c97","ui_kits/mobile-app/ShiftsScreen.jsx":"a4e6e25f0f2f","ui_kits/mobile-app/data.js":"e81ff9bd6901"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.ElmtrackrDesignSystem_2c2e11 = window.ElmtrackrDesignSystem_2c2e11 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/core/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Status pill — the small uppercase chip on shift rows and headers.
 * Each tone maps to an Aurora hour-type hue with a tinted background.
 */
function Badge({
  tone = "neutral",
  dot = false,
  children,
  style = {},
  ...props
}) {
  const tones = {
    neutral: {
      bg: "var(--au-surface-sub)",
      fg: "var(--au-indigo)"
    },
    live: {
      bg: "rgba(16,185,129,0.12)",
      fg: "var(--au-active)"
    },
    overtime: {
      bg: "var(--au-overtime-bg)",
      fg: "var(--au-overtime-ink)"
    },
    weekend: {
      bg: "var(--au-weekend-bg)",
      fg: "var(--au-plum)"
    },
    holiday: {
      bg: "var(--au-weekend-bg)",
      fg: "var(--au-plum)"
    },
    refund: {
      bg: "var(--au-overtime-bg)",
      fg: "var(--au-overtime-ink)"
    }
  };
  const t = tones[tone] || tones.neutral;
  return /*#__PURE__*/React.createElement("span", _extends({
    style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      background: t.bg,
      color: t.fg,
      fontFamily: "var(--au-font)",
      fontSize: "0.625rem",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.06em",
      padding: "2px 8px",
      borderRadius: "var(--radius-pill)",
      lineHeight: 1.5,
      ...style
    }
  }, props), dot && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: 999,
      background: "currentColor",
      animation: tone === "live" ? "auPulse 2s ease-in-out infinite" : undefined
    }
  }), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Elmtrackr primary button. Gradient-filled primary, outlined secondary,
 * solid danger, and quiet ghost — all with the Aurora press-shrink.
 */
function Button({
  variant = "primary",
  size = "md",
  loading = false,
  fullWidth = false,
  disabled = false,
  children,
  style = {},
  ...props
}) {
  const [hover, setHover] = React.useState(false);
  const [press, setPress] = React.useState(false);
  const isDisabled = disabled || loading;
  const sizes = {
    sm: {
      padding: "6px 12px",
      fontSize: "0.875rem",
      borderRadius: "18px"
    },
    md: {
      padding: "10px 16px",
      fontSize: "1rem",
      borderRadius: "18px"
    },
    lg: {
      padding: "14px 24px",
      fontSize: "1rem",
      borderRadius: "18px"
    }
  };
  const base = {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    gap: 8,
    fontFamily: "var(--au-font)",
    fontWeight: 600,
    border: "none",
    cursor: isDisabled ? "not-allowed" : "pointer",
    userSelect: "none",
    width: fullWidth ? "100%" : undefined,
    transition: "transform .15s var(--ease-settle), box-shadow .15s var(--ease-settle), background .15s",
    transform: press && !isDisabled ? "scale(0.98)" : "scale(1)",
    opacity: isDisabled ? 0.5 : 1,
    ...sizes[size]
  };
  const variants = {
    primary: {
      background: "var(--au-grad)",
      color: "#fff",
      boxShadow: isDisabled ? "none" : hover ? "var(--shadow-button-hi)" : "var(--shadow-button)"
    },
    secondary: {
      background: hover ? "var(--au-surface-sub)" : "var(--au-surface)",
      color: "var(--au-indigo)",
      border: `1px solid rgba(91,77,242,${hover ? 0.6 : 0.3})`
    },
    danger: {
      background: hover ? "#DC2626" : "var(--au-danger)",
      color: "#fff",
      boxShadow: "0 6px 14px -6px rgba(239,68,68,0.5)"
    },
    ghost: {
      background: hover ? "var(--au-surface-sub)" : "transparent",
      color: hover ? "var(--au-ink)" : "var(--au-ink-2)"
    }
  };
  return /*#__PURE__*/React.createElement("button", _extends({
    type: "button",
    disabled: isDisabled,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setPress(false);
    },
    onMouseDown: () => setPress(true),
    onMouseUp: () => setPress(false),
    style: {
      ...base,
      ...variants[variant],
      ...style
    }
  }, props), loading && /*#__PURE__*/React.createElement("span", {
    style: {
      width: 16,
      height: 16,
      borderRadius: 999,
      border: "2px solid currentColor",
      borderTopColor: "transparent",
      display: "inline-block",
      animation: "spin .7s linear infinite"
    }
  }), children, /*#__PURE__*/React.createElement("style", null, "@keyframes spin{to{transform:rotate(360deg)}}"));
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Floating white card on the lavender page — 24px radius, hairline border,
 * soft indigo-tinted shadow. The default surface for everything.
 */
function Card({
  padding = "md",
  glass = false,
  glow = false,
  hoverGlow = false,
  children,
  style = {},
  ...props
}) {
  const [hover, setHover] = React.useState(false);
  const pads = {
    none: 0,
    sm: 12,
    md: 16,
    lg: 20
  };
  const lifted = glow || hoverGlow && hover;
  return /*#__PURE__*/React.createElement("div", _extends({
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      borderRadius: "var(--radius-3xl)",
      border: "1px solid rgba(255,255,255,0.8)",
      background: glass ? "var(--au-glass-bg, rgba(236,238,250,0.82))" : "var(--au-surface)",
      backdropFilter: glass ? "blur(var(--blur-glass))" : undefined,
      WebkitBackdropFilter: glass ? "blur(var(--blur-glass))" : undefined,
      boxShadow: lifted ? "var(--shadow-card-glow)" : "var(--shadow-card)",
      padding: pads[padding],
      transition: "box-shadow .25s var(--ease-settle)",
      ...style
    }
  }, props), children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Card.jsx", error: String((e && e.message) || e) }); }

// components/core/Eyebrow.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * The signature uppercase, wide-tracked eyebrow label that sits above
 * every section and stat ("RECENT SHIFTS", "ELAPSED", "THIS MONTH").
 */
function Eyebrow({
  as = "p",
  children,
  style = {},
  ...props
}) {
  const Tag = as;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    style: {
      fontFamily: "var(--au-font)",
      fontSize: "0.75rem",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.16em",
      color: "var(--au-faint)",
      margin: 0,
      ...style
    }
  }, props), children);
}
Object.assign(__ds_scope, { Eyebrow });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Eyebrow.jsx", error: String((e && e.message) || e) }); }

// components/data/ProgressRing.jsx
try { (() => {
/**
 * The signature Aurora progress ring — a gradient arc on a track with an
 * optional comet dot at the tip. Center content via children.
 */
function ProgressRing({
  progress = 0,
  size = 200,
  strokeWidth = 11,
  comet = true,
  gradient = ["#5B4DF2", "#7C5CF6", "#16C8D6"],
  track = "#ECEBFA",
  children,
  style = {}
}) {
  const clamped = Math.min(1, Math.max(0, progress));
  const radius = (size - strokeWidth) / 2;
  const circ = 2 * Math.PI * radius;
  const offset = circ * (1 - clamped);
  const ang = 2 * Math.PI * clamped - Math.PI / 2;
  const cometX = size / 2 + radius * Math.cos(ang);
  const cometY = size / 2 + radius * Math.sin(ang);
  const gid = React.useId();
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      width: size,
      height: size,
      ...style
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: size,
    height: size,
    style: {
      position: "relative",
      transform: "rotate(-90deg)"
    }
  }, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
    id: gid,
    x1: "0",
    y1: "0",
    x2: "1",
    y2: "1"
  }, gradient.map((c, i) => /*#__PURE__*/React.createElement("stop", {
    key: i,
    offset: `${i / (gradient.length - 1) * 100}%`,
    stopColor: c
  })))), /*#__PURE__*/React.createElement("circle", {
    cx: size / 2,
    cy: size / 2,
    r: radius,
    fill: "none",
    stroke: track,
    strokeWidth: strokeWidth
  }), /*#__PURE__*/React.createElement("circle", {
    cx: size / 2,
    cy: size / 2,
    r: radius,
    fill: "none",
    stroke: `url(#${gid})`,
    strokeWidth: strokeWidth,
    strokeLinecap: "round",
    strokeDasharray: circ,
    strokeDashoffset: offset,
    style: {
      transition: "stroke-dashoffset 1s var(--ease-aurora)"
    }
  })), comet && clamped > 0.001 && /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      left: cometX - 9,
      top: cometY - 9,
      width: 18,
      height: 18,
      borderRadius: 999,
      background: "#fff",
      boxShadow: "0 0 0 4px var(--au-pop), 0 4px 16px var(--au-pop)",
      transition: "all 1s var(--ease-aurora)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "absolute",
      inset: 0,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center"
    }
  }, children));
}
Object.assign(__ds_scope, { ProgressRing });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/ProgressRing.jsx", error: String((e && e.message) || e) }); }

// components/data/SegmentedBar.jsx
try { (() => {
/**
 * Horizontal segmented distribution bar + optional legend — used for the
 * hours breakdown (regular / overtime / weekend).
 */
function SegmentedBar({
  segments = [],
  showLegend = false,
  style = {}
}) {
  const total = segments.reduce((s, x) => s + x.value, 0);
  return /*#__PURE__*/React.createElement("div", {
    style: style
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      height: 12,
      borderRadius: 999,
      overflow: "hidden",
      gap: 1,
      background: total === 0 ? "var(--au-surface-sub)" : "transparent"
    }
  }, segments.filter(s => s.value > 0).map((seg, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      width: `${seg.value / total * 100}%`,
      background: seg.color,
      transformOrigin: "left",
      animation: `barExpand .8s var(--ease-settle) ${i * 0.08}s both`
    }
  }))), showLegend && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 8,
      marginTop: 12
    }
  }, segments.map((seg, i) => {
    const pct = total > 0 ? Math.round(seg.value / total * 100) : 0;
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between"
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: "flex",
        alignItems: "center",
        gap: 8
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        width: 8,
        height: 8,
        borderRadius: 999,
        background: seg.color,
        flexShrink: 0
      }
    }), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "var(--au-font)",
        fontSize: "0.875rem",
        color: "var(--au-ink-2)"
      }
    }, seg.label), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "var(--au-font)",
        fontSize: "0.75rem",
        color: "var(--au-faint)"
      }
    }, pct, "%")), seg.display && /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "var(--au-font)",
        fontSize: "0.875rem",
        fontWeight: 600,
        color: "var(--au-ink)"
      }
    }, seg.display));
  })), /*#__PURE__*/React.createElement("style", null, "@keyframes barExpand{from{transform:scaleX(0)}to{transform:scaleX(1)}}"));
}
Object.assign(__ds_scope, { SegmentedBar });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/SegmentedBar.jsx", error: String((e && e.message) || e) }); }

// components/data/StatCard.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * Stat tile — a label + big value, in five tones. `primary` fills with the
 * Aurora gradient; hour-types use their tinted backgrounds.
 */
function StatCard({
  label,
  value,
  sub,
  variant = "default",
  style = {},
  ...props
}) {
  const variants = {
    default: {
      bg: "var(--au-surface)",
      border: "1px solid var(--au-hair)",
      label: "var(--au-ink-2)",
      value: "var(--au-ink)",
      sub: "var(--au-ink-2)",
      shadow: "var(--shadow-card)"
    },
    primary: {
      bg: "var(--au-grad)",
      border: "none",
      label: "rgba(255,255,255,0.8)",
      value: "#fff",
      sub: "rgba(255,255,255,0.7)",
      shadow: "0 16px 30px -14px rgba(91,77,242,0.55)"
    },
    overtime: {
      bg: "var(--au-overtime-bg)",
      border: "1px solid var(--au-hair)",
      label: "var(--au-overtime-ink)",
      value: "var(--au-peach-deep)",
      sub: "var(--au-overtime-ink)",
      shadow: "var(--shadow-card)"
    },
    weekend: {
      bg: "var(--au-weekend-bg)",
      border: "1px solid var(--au-hair)",
      label: "var(--au-plum)",
      value: "var(--au-plum)",
      sub: "var(--au-plum)",
      shadow: "var(--shadow-card)"
    },
    active: {
      bg: "rgba(16,185,129,0.10)",
      border: "1px solid rgba(16,185,129,0.22)",
      label: "var(--au-active)",
      value: "#047857",
      sub: "var(--au-active)",
      shadow: "var(--shadow-card)"
    }
  };
  const v = variants[variant] || variants.default;
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 4,
      borderRadius: "var(--radius-3xl)",
      padding: 16,
      background: v.bg,
      border: v.border,
      boxShadow: v.shadow,
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-font)",
      fontSize: "0.75rem",
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: "0.06em",
      color: v.label
    }
  }, label), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-display)",
      fontSize: "1.5rem",
      fontWeight: 800,
      lineHeight: 1.1,
      letterSpacing: "-0.02em",
      color: v.value
    }
  }, value), sub && /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-font)",
      fontSize: "0.75rem",
      fontWeight: 500,
      color: v.sub
    }
  }, sub));
}
Object.assign(__ds_scope, { StatCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/StatCard.jsx", error: String((e && e.message) || e) }); }

// components/feedback/EmptyState.jsx
try { (() => {
/** Centered empty state — icon, title, description, optional action. */
function EmptyState({
  icon = "📋",
  title,
  description,
  action,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      textAlign: "center",
      padding: "64px 24px",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    "aria-hidden": true,
    style: {
      fontSize: "2.25rem",
      marginBottom: 12
    }
  }, icon), /*#__PURE__*/React.createElement("h3", {
    style: {
      margin: 0,
      fontFamily: "var(--au-font)",
      fontSize: "1rem",
      fontWeight: 600,
      color: "var(--au-ink)"
    }
  }, title), description && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px 0 0",
      maxWidth: "20rem",
      fontFamily: "var(--au-font)",
      fontSize: "0.875rem",
      color: "var(--au-ink-2)"
    }
  }, description), action && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 16
    }
  }, action));
}
Object.assign(__ds_scope, { EmptyState });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/EmptyState.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Toast.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Single toast — colored chip with an icon badge. Compose your own stack. */
function Toast({
  type = "info",
  children,
  style = {},
  ...props
}) {
  const cfg = {
    success: {
      bg: "#059669",
      icon: "✓"
    },
    error: {
      bg: "var(--au-danger)",
      icon: "✕"
    },
    info: {
      bg: "#4338CA",
      icon: "·"
    }
  }[type] || {
    bg: "#4338CA",
    icon: "·"
  };
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      alignItems: "center",
      gap: 12,
      borderRadius: "var(--radius-2xl)",
      padding: "12px 16px",
      background: cfg.bg,
      boxShadow: "0 18px 40px -16px rgba(0,0,0,0.4)",
      animation: "fade-in-up .22s var(--ease-settle) both",
      ...style
    }
  }, props), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 20,
      height: 20,
      borderRadius: 999,
      background: "rgba(255,255,255,0.2)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "0.75rem",
      fontWeight: 700,
      color: "#fff"
    }
  }, cfg.icon), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-font)",
      fontSize: "0.875rem",
      fontWeight: 600,
      color: "#fff"
    }
  }, children));
}
Object.assign(__ds_scope, { Toast });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Toast.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Labelled text input — inset sub-surface fill, indigo focus ring, error/hint states. */
function Input({
  label,
  error,
  hint,
  id,
  style = {},
  ...props
}) {
  const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, "-") : undefined);
  const [focus, setFocus] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 6
    }
  }, label && /*#__PURE__*/React.createElement("label", {
    htmlFor: inputId,
    style: {
      fontFamily: "var(--au-font)",
      fontSize: "0.875rem",
      fontWeight: 600,
      color: "var(--au-ink-2)"
    }
  }, label), /*#__PURE__*/React.createElement("input", _extends({
    id: inputId,
    onFocus: e => {
      setFocus(true);
      props.onFocus?.(e);
    },
    onBlur: e => {
      setFocus(false);
      props.onBlur?.(e);
    },
    style: {
      width: "100%",
      boxSizing: "border-box",
      borderRadius: "var(--radius-md)",
      padding: "10px 16px",
      fontSize: "0.875rem",
      fontFamily: "var(--au-font)",
      color: "var(--au-ink)",
      background: error ? "rgba(239,68,68,0.06)" : "var(--au-surface-sub)",
      border: `1px solid ${error ? "rgba(239,68,68,0.5)" : focus ? "var(--au-indigo)" : "var(--au-hair)"}`,
      outline: "none",
      boxShadow: focus ? `0 0 0 2px ${error ? "rgba(239,68,68,0.25)" : "rgba(91,77,242,0.25)"}` : "none",
      transition: "border-color .15s, box-shadow .15s",
      ...style
    }
  }, props)), error && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: "0.75rem",
      fontWeight: 500,
      color: "var(--au-danger)"
    }
  }, error), hint && !error && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: "0.75rem",
      color: "var(--au-faint)"
    }
  }, hint));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// components/forms/Segmented.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/** Segmented control — the pill toggle used for theme / tab switches. */
function Segmented({
  options = [],
  value,
  onChange,
  style = {},
  ...props
}) {
  return /*#__PURE__*/React.createElement("div", _extends({
    style: {
      display: "flex",
      gap: 4,
      padding: 4,
      borderRadius: "var(--radius-3xl)",
      background: "var(--au-surface)",
      border: "1px solid rgba(255,255,255,0.8)",
      boxShadow: "var(--shadow-card)",
      ...style
    }
  }, props), options.map(opt => {
    const val = typeof opt === "string" ? opt : opt.value;
    const label = typeof opt === "string" ? opt : opt.label;
    const active = val === value;
    return /*#__PURE__*/React.createElement("button", {
      key: val,
      type: "button",
      onClick: () => onChange?.(val),
      style: {
        flex: 1,
        border: "none",
        cursor: "pointer",
        borderRadius: "var(--radius-2xl)",
        padding: "8px 12px",
        fontFamily: "var(--au-font)",
        fontSize: "0.875rem",
        fontWeight: 700,
        transition: "all .2s var(--ease-settle)",
        background: active ? "var(--au-grad)" : "transparent",
        color: active ? "#fff" : "var(--au-faint)",
        boxShadow: active ? "0 6px 14px -6px rgba(91,77,242,0.5)" : "none"
      }
    }, label);
  }));
}
Object.assign(__ds_scope, { Segmented });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Segmented.jsx", error: String((e && e.message) || e) }); }

// components/navigation/BottomNav.jsx
try { (() => {
const ICONS = {
  home: "M3 10.5 12 3l9 7.5M5.5 9.5V20a1 1 0 0 0 1 1H10v-5.5h4V21h3.5a1 1 0 0 0 1-1V9.5",
  list: "M8 4h8a1 1 0 0 1 1 1v0a2 2 0 0 1-2 2H9A2 2 0 0 1 7 5v0a1 1 0 0 1 1-1ZM7 6H6a2 2 0 0 0-2 2v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-1M9 12h6M9 16h4",
  chart: "M5 21V11M12 21V4M19 21v-7",
  settings: "M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z M19.4 13a7.6 7.6 0 0 0 .1-1 7.6 7.6 0 0 0-.1-1l1.7-1.3-2-3.4-2 .8a7.3 7.3 0 0 0-1.7-1l-.3-2.1H9.9l-.3 2.1a7.3 7.3 0 0 0-1.7 1l-2-.8-2 3.4L5.6 11a7.6 7.6 0 0 0 0 2l-1.7 1.3 2 3.4 2-.8a7.3 7.3 0 0 0 1.7 1l.3 2.1h4.2l.3-2.1a7.3 7.3 0 0 0 1.7-1l2 .8 2-3.4Z"
};

/**
 * Frosted bottom tab bar with a gradient pill behind the active icon.
 * The app's primary navigation surface.
 */
function BottomNav({
  items = [{
    id: "home",
    label: "Home",
    icon: "home"
  }, {
    id: "shifts",
    label: "Shifts",
    icon: "list"
  }, {
    id: "reports",
    label: "Reports",
    icon: "chart"
  }, {
    id: "settings",
    label: "Settings",
    icon: "settings"
  }],
  active = "home",
  onSelect,
  fixed = false,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("nav", {
    style: {
      position: fixed ? "fixed" : "relative",
      bottom: fixed ? 0 : undefined,
      left: 0,
      right: 0,
      zIndex: 40,
      background: "var(--au-surface)",
      backdropFilter: "blur(var(--blur-nav))",
      WebkitBackdropFilter: "blur(var(--blur-nav))",
      borderTop: "1px solid var(--au-hair)",
      boxShadow: "var(--shadow-nav)",
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      maxWidth: "28rem",
      margin: "0 auto",
      padding: "0 8px"
    }
  }, items.map(it => {
    const isActive = it.id === active;
    return /*#__PURE__*/React.createElement("button", {
      key: it.id,
      type: "button",
      onClick: () => onSelect?.(it.id),
      "aria-current": isActive ? "page" : undefined,
      style: {
        flex: 1,
        border: "none",
        background: "transparent",
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 4,
        padding: "10px 0",
        minHeight: 48
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        width: 48,
        height: 32,
        borderRadius: 13,
        background: isActive ? "var(--au-grad)" : "transparent",
        boxShadow: isActive ? "var(--shadow-pill)" : "none",
        transition: "all .25s var(--ease-settle)"
      }
    }, /*#__PURE__*/React.createElement("svg", {
      width: "20",
      height: "20",
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: isActive ? "#fff" : "var(--au-ink-2)",
      strokeWidth: isActive ? 2.2 : 2,
      strokeLinecap: "round",
      strokeLinejoin: "round"
    }, /*#__PURE__*/React.createElement("path", {
      d: ICONS[it.icon] || ICONS.home
    }))), /*#__PURE__*/React.createElement("span", {
      style: {
        fontFamily: "var(--au-font)",
        fontSize: "10.5px",
        fontWeight: 600,
        color: isActive ? "var(--au-indigo)" : "var(--au-ink-2)"
      }
    }, it.label));
  })));
}
Object.assign(__ds_scope, { BottomNav });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/navigation/BottomNav.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/HomeScreen.jsx
try { (() => {
// HomeScreen — the dashboard with the interactive clock widget.
const {
  ProgressRing,
  Eyebrow,
  Card
} = window.ElmtrackrDesignSystem_2c2e11;
function fmtHMS(total) {
  const h = Math.floor(total / 3600),
    m = Math.floor(total % 3600 / 60),
    s = total % 60;
  const p = n => String(n).padStart(2, "0");
  return h > 0 ? `${p(h)}:${p(m)}:${p(s)}` : `${p(m)}:${p(s)}`;
}
function ClockWidget() {
  const [clockedIn, setClockedIn] = React.useState(false);
  const [elapsed, setElapsed] = React.useState(0);
  const [bloom, setBloom] = React.useState(false);
  const startRef = React.useRef(0);
  const goal = 8 * 3600;
  React.useEffect(() => {
    if (!clockedIn) return;
    const id = setInterval(() => setElapsed(Math.floor((Date.now() - startRef.current) / 1000)), 1000);
    return () => clearInterval(id);
  }, [clockedIn]);
  const progress = clockedIn ? Math.min(1, elapsed / goal) : 0;
  const isOT = elapsed > goal;
  function toggle() {
    if (clockedIn) {
      setClockedIn(false);
      setElapsed(0);
    } else {
      startRef.current = Date.now();
      setElapsed(0);
      setClockedIn(true);
      setBloom(true);
      setTimeout(() => setBloom(false), 900);
    }
  }
  const now = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });
  return /*#__PURE__*/React.createElement("div", {
    className: "au-grain",
    style: {
      position: "relative",
      borderRadius: 24,
      overflow: "hidden",
      background: "#fff",
      border: "1px solid rgba(255,255,255,.9)",
      boxShadow: "var(--shadow-card)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    className: "au-mesh",
    "aria-hidden": true,
    style: {
      position: "absolute",
      inset: "-12%",
      filter: "blur(8px)",
      background: "radial-gradient(38% 32% at 18% 14%, rgba(91,77,242,.22), transparent 70%), radial-gradient(40% 36% at 88% 8%, rgba(124,92,246,.20), transparent 72%), radial-gradient(46% 40% at 78% 92%, rgba(22,200,214,.18), transparent 72%), radial-gradient(44% 38% at 8% 88%, rgba(124,92,246,.18), transparent 72%)"
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative",
      zIndex: 1,
      padding: 20,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 8,
      borderRadius: 999,
      padding: "6px 16px",
      fontSize: 12,
      fontWeight: 700,
      letterSpacing: ".12em",
      textTransform: "uppercase",
      background: clockedIn ? "var(--au-grad)" : "var(--au-surface-sub)",
      color: clockedIn ? "#fff" : "var(--au-faint)",
      boxShadow: clockedIn ? "var(--shadow-pill)" : "none"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 6,
      height: 6,
      borderRadius: 999,
      background: clockedIn ? "#fff" : "var(--au-faint)",
      boxShadow: clockedIn ? "0 0 0 3px rgba(255,255,255,.32)" : "none",
      animation: clockedIn ? "auPulse 2s ease-in-out infinite" : "none"
    }
  }), clockedIn ? "On Shift · Regular" : "Not Clocked In"), /*#__PURE__*/React.createElement("div", {
    style: {
      position: "relative"
    }
  }, bloom && /*#__PURE__*/React.createElement("div", {
    "aria-hidden": true,
    style: {
      position: "absolute",
      inset: 0,
      borderRadius: "50%",
      border: "10px solid #7C5CF6",
      animation: "auBloom .9s cubic-bezier(0.2,0.6,0.3,1) forwards",
      pointerEvents: "none"
    }
  }), /*#__PURE__*/React.createElement(ProgressRing, {
    progress: progress,
    size: 200,
    comet: clockedIn
  }, clockedIn ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 4
    }
  }, "Elapsed"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-display)",
      fontSize: elapsed >= 3600 ? 32 : 40,
      fontWeight: 700,
      letterSpacing: "-.03em",
      color: "var(--au-ink)",
      fontVariantNumeric: "tabular-nums"
    }
  }, fmtHMS(elapsed)), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      color: "var(--au-ink-2)",
      marginTop: 4
    }
  }, "since ", /*#__PURE__*/React.createElement("b", {
    style: {
      color: "var(--au-ink)"
    }
  }, new Date(startRef.current).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  })))) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: "var(--au-display)",
      fontSize: 36,
      fontWeight: 700,
      letterSpacing: "-.03em",
      color: "var(--au-ink)",
      fontVariantNumeric: "tabular-nums"
    }
  }, now), /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginTop: 4
    }
  }, "Ready")))), clockedIn && /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      width: "100%"
    }
  }, [["Daily Goal", "8h"], ["Progress", `${Math.round(progress * 100)}%${isOT ? " OT" : ""}`], ["Started", new Date(startRef.current).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  })]].map(([k, v], i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      flex: 1,
      borderRadius: 15,
      padding: "10px 12px",
      background: "var(--au-surface-sub)"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: ".1em",
      color: "var(--au-faint)",
      marginBottom: 2
    }
  }, k), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 16,
      fontWeight: 700,
      color: i === 1 && isOT ? "var(--au-peach-deep)" : i === 1 ? "var(--au-indigo)" : "var(--au-ink)"
    }
  }, v)))), !clockedIn && /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 14,
      color: "var(--au-ink-2)"
    }
  }, "Tap to start tracking your shift"), /*#__PURE__*/React.createElement("button", {
    onClick: toggle,
    style: {
      width: "100%",
      borderRadius: 18,
      padding: "16px 0",
      fontSize: 16,
      fontWeight: 700,
      letterSpacing: ".02em",
      cursor: "pointer",
      transition: "transform .1s",
      ...(clockedIn ? {
        background: "transparent",
        color: "var(--au-indigo)",
        border: "1.5px solid var(--au-indigo)"
      } : {
        background: "var(--au-grad)",
        color: "#fff",
        border: "none",
        boxShadow: "var(--shadow-button)"
      })
    }
  }, clockedIn ? "Clock Out" : "Clock In")));
}
function HomeScreen() {
  const {
    month,
    fmtCurrency
  } = window.ELM;
  const recent = window.ELM.shifts.slice(0, 4);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      paddingTop: 4
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Eyebrow, null, "Good morning \xB7 Avi"), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: "4px 0 0",
      display: "flex",
      alignItems: "center",
      gap: 8,
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 700,
      letterSpacing: "-.03em",
      color: "var(--au-ink)"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 22,
      height: 22,
      borderRadius: 7,
      background: "var(--au-grad)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      boxShadow: "0 6px 14px -6px rgba(91,77,242,.7)"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "12",
    height: "12",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "#fff",
    strokeWidth: "2.4",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M13 2 4 14h6l-1 8 9-12h-6l1-8Z"
  }))), "elmtrackr")), /*#__PURE__*/React.createElement("button", {
    style: {
      width: 40,
      height: 40,
      borderRadius: 999,
      border: "none",
      background: "#fff",
      boxShadow: "0 6px 16px -8px rgba(40,30,90,.25)",
      color: "var(--au-ink-2)",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "17",
    height: "17",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2",
    strokeLinecap: "round",
    strokeLinejoin: "round"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M9 21H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3M16 17l5-5-5-5M21 12H9"
  })))), /*#__PURE__*/React.createElement(ClockWidget, null), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, null, "This Month \xB7 Estimated Gross"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 2px",
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 800,
      letterSpacing: "-.02em"
    },
    className: "au-gradient-text"
  }, fmtCurrency(month.gross)), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 12px",
      fontSize: 10,
      color: "var(--au-faint)"
    }
  }, "Estimate only \u2014 confirm against your payslip."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8
    }
  }, [["Regular", fmtCurrency(month.regularGross), "var(--au-surface-sub)", "var(--au-ink)", "var(--au-faint)"], ["Overtime", fmtCurrency(month.overtimeGross), "var(--au-overtime-bg)", "var(--au-peach-deep)", "var(--au-overtime-ink)"], ["Holiday", fmtCurrency(month.holidayGross), "var(--au-weekend-bg)", "var(--au-plum)", "var(--au-plum)"]].map(([k, v, bg, vc, lc]) => /*#__PURE__*/React.createElement("div", {
    key: k,
    style: {
      flex: 1,
      borderRadius: 15,
      padding: 10,
      background: bg
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 9,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: lc
    }
  }, k), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "2px 0 0",
      fontSize: 14,
      fontWeight: 700,
      color: vc
    }
  }, v))))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0 4px",
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    as: "h2"
  }, "Recent Shifts"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      fontWeight: 700,
      color: "var(--au-indigo)",
      cursor: "pointer"
    }
  }, "View all \u2192")), /*#__PURE__*/React.createElement(Card, {
    padding: "none",
    style: {
      overflow: "hidden"
    }
  }, recent.map((s, i) => /*#__PURE__*/React.createElement(window.ShiftRow, {
    key: s.id,
    shift: s,
    last: i === recent.length - 1
  })))), /*#__PURE__*/React.createElement("button", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: 8,
      borderRadius: 24,
      padding: "16px 0",
      border: "1.5px dashed var(--au-hair)",
      background: "rgba(255,255,255,.5)",
      color: "var(--au-indigo)",
      cursor: "pointer",
      fontFamily: "var(--au-font)",
      fontSize: 14,
      fontWeight: 600
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 20,
      height: 20,
      borderRadius: 8,
      background: "var(--au-surface-sub)",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontWeight: 700
    }
  }, "+"), "Add shift manually"));
}
window.HomeScreen = HomeScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/HomeScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/ReportsScreen.jsx
try { (() => {
// ReportsScreen — hours distribution, stat grid, gross estimate, breakdown.
const {
  Eyebrow,
  Card,
  StatCard,
  SegmentedBar,
  Segmented,
  Button
} = window.ElmtrackrDesignSystem_2c2e11;
function ReportsScreen() {
  const {
    month,
    fmtHours,
    fmtCurrency
  } = window.ELM;
  const [tab, setTab] = React.useState("hours");
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: "4px 0 0",
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 700,
      letterSpacing: "-.02em",
      color: "var(--au-ink)"
    }
  }, "Reports"), /*#__PURE__*/React.createElement(Segmented, {
    options: [{
      value: "hours",
      label: "Hours"
    }, {
      value: "refunds",
      label: "Travel Refunds"
    }],
    value: tab,
    onChange: setTab
  }), /*#__PURE__*/React.createElement(Card, {
    padding: "none",
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "8px 12px"
    }
  }, /*#__PURE__*/React.createElement("button", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 12,
      border: "none",
      background: "var(--au-surface-sub)",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--au-ink-2)"
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2.5"
  }, /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M15 19l-7-7 7-7"
  }))), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 14,
      fontWeight: 700,
      color: "var(--au-ink)"
    }
  }, "June 2026"), /*#__PURE__*/React.createElement("button", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 12,
      border: "none",
      background: "var(--au-surface-sub)",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: "var(--au-ink-2)",
      opacity: 0.3
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "16",
    height: "16",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2.5"
  }, /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M9 5l7 7-7 7"
  })))), tab === "refunds" ? /*#__PURE__*/React.createElement(Card, {
    padding: "lg",
    style: {
      textAlign: "center"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 36,
      marginBottom: 8
    }
  }, "\uD83E\uDDFE"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 16,
      fontWeight: 600,
      color: "var(--au-ink)"
    }
  }, "2 travel refunds pending"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px auto 16px",
      maxWidth: 240,
      fontSize: 14,
      color: "var(--au-ink-2)"
    }
  }, "File your transport claims before month end to get reimbursed."), /*#__PURE__*/React.createElement(Button, {
    variant: "primary",
    size: "md"
  }, "Review refunds")) : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      marginBottom: 12
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Eyebrow, null, "Hours Distribution"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px 0 0",
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 800,
      letterSpacing: "-.02em",
      color: "var(--au-ink)"
    }
  }, fmtHours(month.totalMins), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 16,
      color: "var(--au-faint)",
      marginLeft: 2
    }
  }, "h")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "2px 0 0",
      fontSize: 12,
      color: "var(--au-faint)"
    }
  }, month.shiftCount, " shifts")), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "sm"
  }, /*#__PURE__*/React.createElement("svg", {
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2"
  }, /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
  })), "CSV")), /*#__PURE__*/React.createElement(SegmentedBar, {
    showLegend: true,
    segments: [{
      label: "Regular",
      value: month.regularMins,
      color: "#5B4DF2",
      display: fmtHours(month.regularMins) + "h"
    }, {
      label: "Overtime",
      value: month.overtimeMins,
      color: "#FF9E7D",
      display: fmtHours(month.overtimeMins) + "h"
    }, {
      label: "Weekend",
      value: month.weekendMins,
      color: "#8B5CF6",
      display: fmtHours(month.weekendMins) + "h"
    }]
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr",
      gap: 12
    }
  }, /*#__PURE__*/React.createElement(StatCard, {
    label: "Total",
    value: fmtHours(month.totalMins) + "h",
    variant: "primary"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Regular",
    value: fmtHours(month.regularMins) + "h",
    variant: "default"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Overtime",
    value: fmtHours(month.overtimeMins) + "h",
    variant: "overtime"
  }), /*#__PURE__*/React.createElement(StatCard, {
    label: "Weekend",
    value: fmtHours(month.weekendMins) + "h",
    variant: "weekend"
  })), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, null, "Estimated Gross Compensation"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 12px",
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 800,
      letterSpacing: "-.02em"
    },
    className: "au-gradient-text"
  }, fmtCurrency(month.gross)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "grid",
      gridTemplateColumns: "1fr 1fr 1fr",
      gap: 8
    }
  }, [["Regular", fmtCurrency(month.regularGross), "var(--au-surface-sub)", "var(--au-indigo)", "var(--au-faint)"], ["Overtime", fmtCurrency(month.overtimeGross), "var(--au-overtime-bg)", "var(--au-peach-deep)", "var(--au-overtime-ink)"], ["Holiday", fmtCurrency(month.holidayGross), "var(--au-weekend-bg)", "var(--au-plum)", "var(--au-plum)"]].map(([k, v, bg, vc, lc]) => /*#__PURE__*/React.createElement("div", {
    key: k,
    style: {
      borderRadius: 16,
      padding: 10,
      textAlign: "center",
      background: bg
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 10,
      fontWeight: 700,
      textTransform: "uppercase",
      letterSpacing: ".06em",
      color: lc
    }
  }, k), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "2px 0 0",
      fontSize: 14,
      fontWeight: 800,
      color: vc
    }
  }, v)))))));
}
window.ReportsScreen = ReportsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/ReportsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/SettingsScreen.jsx
try { (() => {
// SettingsScreen — appearance, profile, thresholds, weekend days.
const {
  Eyebrow,
  Card,
  Input,
  Segmented,
  Button
} = window.ElmtrackrDesignSystem_2c2e11;
function SettingsScreen({
  theme,
  onTheme
}) {
  const [weekend, setWeekend] = React.useState([5, 6]);
  const days = [["Sun", 0], ["Mon", 1], ["Tue", 2], ["Wed", 3], ["Thu", 4], ["Fri", 5], ["Sat", 6]];
  const toggle = d => setWeekend(w => w.includes(d) ? w.filter(x => x !== d) : [...w, d]);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      paddingTop: 4
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 700,
      letterSpacing: "-.02em",
      color: "var(--au-ink)"
    }
  }, "Settings"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "8px 0 0",
      fontSize: 14,
      color: "var(--au-ink-2)"
    }
  }, "Theme saves immediately. Other changes use the save bar.")), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 12
    }
  }, "Appearance"), /*#__PURE__*/React.createElement("label", {
    style: {
      display: "block",
      fontSize: 14,
      fontWeight: 600,
      color: "var(--au-ink-2)",
      marginBottom: 6
    }
  }, "Theme"), /*#__PURE__*/React.createElement(Segmented, {
    options: [{
      value: "system",
      label: "System"
    }, {
      value: "light",
      label: "Light"
    }, {
      value: "dark",
      label: "Dark"
    }],
    value: theme,
    onChange: onTheme
  })), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 4
    }
  }, "Profile"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 14px",
      fontSize: 12,
      color: "var(--au-faint)"
    }
  }, "Your name is used for the greeting on the home screen."), /*#__PURE__*/React.createElement(Input, {
    label: "Display name",
    defaultValue: "Avi",
    hint: "First name or nickname \u2014 whatever you prefer"
  })), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 14
    }
  }, "Overtime Thresholds"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 14
    }
  }, /*#__PURE__*/React.createElement(Input, {
    label: "Daily overtime after (hours)",
    type: "number",
    defaultValue: "8",
    hint: "Overtime kicks in after this many hours in a single shift"
  }), /*#__PURE__*/React.createElement(Input, {
    label: "Weekly overtime after (hours)",
    type: "number",
    defaultValue: "42",
    hint: "Overtime kicks in after this many total hours per week"
  }))), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 4
    }
  }, "Weekend Days"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 14px",
      fontSize: 12,
      color: "var(--au-faint)"
    }
  }, "Select which days count as weekend. Default: Friday & Saturday."), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      gap: 8,
      flexWrap: "wrap"
    }
  }, days.map(([label, d]) => {
    const on = weekend.includes(d);
    return /*#__PURE__*/React.createElement("button", {
      key: d,
      onClick: () => toggle(d),
      style: {
        borderRadius: 12,
        padding: "8px 12px",
        fontSize: 14,
        fontWeight: 700,
        cursor: "pointer",
        border: "none",
        transition: "all .15s",
        background: on ? "var(--au-grad)" : "var(--au-surface-sub)",
        color: on ? "#fff" : "var(--au-faint)",
        boxShadow: on ? "var(--shadow-pill)" : "none"
      }
    }, label);
  }))), /*#__PURE__*/React.createElement(Card, {
    padding: "md"
  }, /*#__PURE__*/React.createElement(Eyebrow, {
    style: {
      marginBottom: 4
    }
  }, "Base Rate"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "0 0 14px",
      fontSize: 12,
      color: "var(--au-faint)"
    }
  }, "Set your hourly base rate to see estimated gross pay."), /*#__PURE__*/React.createElement(Input, {
    label: "Hourly base rate",
    type: "number",
    defaultValue: "45.00",
    hint: "Used for estimated compensation based on your profile rules"
  })), /*#__PURE__*/React.createElement(Button, {
    variant: "ghost",
    fullWidth: true,
    style: {
      color: "var(--au-danger)"
    }
  }, "Sign Out"));
}
window.SettingsScreen = SettingsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/SettingsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/ShiftRow.jsx
try { (() => {
// ShiftRow — product-specific list row composing the Badge primitive.
const {
  Badge
} = window.ElmtrackrDesignSystem_2c2e11;
function ShiftRow({
  shift,
  last
}) {
  const [hover, setHover] = React.useState(false);
  const stripe = {
    regular: {
      c: "var(--au-indigo)",
      o: 0.3
    },
    overtime: {
      c: "var(--au-indigo)",
      o: 0.3
    },
    weekend: {
      c: "var(--au-plum)",
      o: 1
    },
    holiday: {
      c: "var(--au-plum)",
      o: 1
    },
    overnight: {
      c: "var(--au-indigo)",
      o: 0.75
    }
  }[shift.type] || {
    c: "var(--au-indigo)",
    o: 0.3
  };
  const badgeLabel = {
    overtime: "Overtime",
    weekend: "Weekend",
    holiday: "Holiday",
    neutral: "Overnight"
  };
  return /*#__PURE__*/React.createElement("div", {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: "flex",
      alignItems: "stretch",
      gap: 0,
      cursor: "pointer",
      borderBottom: last ? "none" : "1px solid var(--au-hair)",
      background: hover ? "var(--au-surface-sub)" : "transparent",
      transition: "background .15s"
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 4,
      flexShrink: 0,
      background: stripe.c,
      opacity: stripe.o
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0,
      width: 56,
      textAlign: "center",
      padding: "14px 0 14px 12px"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontFamily: "var(--au-display)",
      fontSize: 16,
      fontWeight: 800,
      lineHeight: 1,
      color: "var(--au-ink)"
    }
  }, String(shift.day).padStart(2, "0")), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "3px 0 0",
      fontSize: 10,
      fontWeight: 600,
      textTransform: "uppercase",
      letterSpacing: ".04em",
      color: "var(--au-faint)"
    }
  }, shift.weekday)), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0,
      padding: "14px 8px"
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 14,
      fontWeight: 600,
      color: "var(--au-ink)"
    }
  }, shift.start, " \u2014 ", shift.end), /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      gap: 6,
      marginTop: 5,
      flexWrap: "wrap"
    }
  }, shift.badges.map(b => /*#__PURE__*/React.createElement(Badge, {
    key: b,
    tone: b
  }, badgeLabel[b] || b)), shift.notes && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      color: "var(--au-faint)"
    }
  }, shift.notes))), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0,
      textAlign: "right",
      padding: "14px 12px 14px 0"
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      margin: 0,
      fontSize: 14,
      fontWeight: 700,
      color: "var(--au-ink)"
    }
  }, window.ELM.fmtMinutes(shift.mins)), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "2px 0 0",
      fontSize: 10,
      fontWeight: 700,
      color: "var(--au-indigo)"
    }
  }, window.ELM.fmtCurrency(shift.pay))), /*#__PURE__*/React.createElement("svg", {
    style: {
      alignSelf: "center",
      marginRight: 12,
      flexShrink: 0,
      color: "var(--au-faint)"
    },
    width: "14",
    height: "14",
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: "2.5"
  }, /*#__PURE__*/React.createElement("path", {
    strokeLinecap: "round",
    strokeLinejoin: "round",
    d: "M9 5l7 7-7 7"
  })));
}
window.ShiftRow = ShiftRow;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/ShiftRow.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/ShiftsScreen.jsx
try { (() => {
// ShiftsScreen — the full shift list grouped under the month.
const {
  Eyebrow,
  Card
} = window.ElmtrackrDesignSystem_2c2e11;
function ShiftsScreen() {
  const {
    shifts,
    month,
    fmtHours,
    fmtCurrency
  } = window.ELM;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      flexDirection: "column",
      gap: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      paddingTop: 4
    }
  }, /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontFamily: "var(--au-display)",
      fontSize: 30,
      fontWeight: 700,
      letterSpacing: "-.02em",
      color: "var(--au-ink)"
    }
  }, "Shifts"), /*#__PURE__*/React.createElement("button", {
    style: {
      width: 40,
      height: 40,
      borderRadius: 999,
      border: "none",
      background: "var(--au-grad)",
      boxShadow: "var(--shadow-pill)",
      color: "#fff",
      cursor: "pointer",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 22,
      fontWeight: 400,
      lineHeight: 1
    }
  }, "+")), /*#__PURE__*/React.createElement(Card, {
    padding: "md",
    style: {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center"
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Eyebrow, null, "June 2026"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px 0 0",
      fontFamily: "var(--au-display)",
      fontSize: 24,
      fontWeight: 800,
      letterSpacing: "-.02em",
      color: "var(--au-ink)"
    }
  }, fmtHours(month.totalMins), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 14,
      color: "var(--au-faint)",
      marginLeft: 2
    }
  }, "h"))), /*#__PURE__*/React.createElement("div", {
    style: {
      textAlign: "right"
    }
  }, /*#__PURE__*/React.createElement(Eyebrow, null, month.shiftCount, " shifts"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: "4px 0 0",
      fontFamily: "var(--au-display)",
      fontSize: 24,
      fontWeight: 800,
      letterSpacing: "-.02em"
    },
    className: "au-gradient-text"
  }, fmtCurrency(month.gross)))), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(Eyebrow, {
    as: "h2",
    style: {
      padding: "0 4px",
      marginBottom: 8
    }
  }, "All Shifts \xB7 June"), /*#__PURE__*/React.createElement(Card, {
    padding: "none",
    style: {
      overflow: "hidden"
    }
  }, shifts.map((s, i) => /*#__PURE__*/React.createElement(window.ShiftRow, {
    key: s.id,
    shift: s,
    last: i === shifts.length - 1
  })))));
}
window.ShiftsScreen = ShiftsScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/ShiftsScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mobile-app/data.js
try { (() => {
// Elmtrackr mobile UI kit — fake data + formatters. Plain script → window.ELM.
(function () {
  function fmtCurrency(n) {
    return "₪" + n.toLocaleString("en-US", {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    });
  }
  function fmtMinutes(mins) {
    const h = Math.floor(mins / 60),
      m = mins % 60;
    return h > 0 ? m > 0 ? `${h}h ${m}m` : `${h}h` : `${m}m`;
  }
  function fmtHours(mins, dp = 1) {
    return (mins / 60).toFixed(dp);
  }

  // Recent shifts (most recent first). type: regular | overtime | weekend | holiday | overnight
  const shifts = [{
    id: 1,
    day: 14,
    weekday: "Mon",
    start: "09:02",
    end: "18:30",
    mins: 508,
    type: "overtime",
    pay: 612,
    badges: ["overtime"],
    notes: ""
  }, {
    id: 2,
    day: 13,
    weekday: "Sun",
    start: "08:45",
    end: "16:50",
    mins: 425,
    type: "regular",
    pay: 510,
    badges: [],
    notes: "Inventory"
  }, {
    id: 3,
    day: 11,
    weekday: "Fri",
    start: "10:00",
    end: "19:15",
    mins: 495,
    type: "weekend",
    pay: 743,
    badges: ["weekend"],
    notes: ""
  }, {
    id: 4,
    day: 10,
    weekday: "Thu",
    start: "22:00",
    end: "06:10",
    mins: 430,
    type: "overnight",
    pay: 645,
    badges: ["neutral"],
    notes: "Night cover"
  }, {
    id: 5,
    day: 8,
    weekday: "Tue",
    start: "09:00",
    end: "17:00",
    mins: 450,
    type: "regular",
    pay: 540,
    badges: [],
    notes: ""
  }, {
    id: 6,
    day: 7,
    weekday: "Mon",
    start: "09:05",
    end: "17:30",
    mins: 475,
    type: "regular",
    pay: 570,
    badges: [],
    notes: ""
  }, {
    id: 7,
    day: 4,
    weekday: "Fri",
    start: "11:00",
    end: "20:00",
    mins: 480,
    type: "weekend",
    pay: 720,
    badges: ["weekend"],
    notes: ""
  }];
  const month = {
    label: "JUNE",
    totalMins: 9620,
    regularMins: 7800,
    overtimeMins: 980,
    weekendMins: 840,
    shiftCount: 21,
    gross: 8420,
    regularGross: 6240,
    overtimeGross: 1180,
    holidayGross: 1000
  };
  window.ELM = {
    shifts,
    month,
    fmtCurrency,
    fmtMinutes,
    fmtHours
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mobile-app/data.js", error: String((e && e.message) || e) }); }

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Eyebrow = __ds_scope.Eyebrow;

__ds_ns.ProgressRing = __ds_scope.ProgressRing;

__ds_ns.SegmentedBar = __ds_scope.SegmentedBar;

__ds_ns.StatCard = __ds_scope.StatCard;

__ds_ns.EmptyState = __ds_scope.EmptyState;

__ds_ns.Toast = __ds_scope.Toast;

__ds_ns.Input = __ds_scope.Input;

__ds_ns.Segmented = __ds_scope.Segmented;

__ds_ns.BottomNav = __ds_scope.BottomNav;

})();
