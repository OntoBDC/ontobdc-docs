/**
 * i18n-helpers.js
 * Client-side internationalization for OntoBDC.
 * Detects browser language (or stored preference) and applies translations
 * to all elements with [data-i18n] attributes.
 */
(function () {
  var STORAGE_KEY = "ob-lang-preference";
  var DEFAULT_LANG = "en";
  var SUPPORTED = ["en", "pt", "es"];

  function detectLanguage() {
    // 1. Check stored preference
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED.indexOf(stored) !== -1) {
        return stored;
      }
    } catch (e) {}

    // 2. Detect from browser
    var browser = (navigator.language || "en").toLowerCase();
    for (var i = 0; i < SUPPORTED.length; i++) {
      if (browser.indexOf(SUPPORTED[i]) === 0) {
        return SUPPORTED[i];
      }
    }
    return DEFAULT_LANG;
  }

  function setLanguage(lang, persist) {
    if (SUPPORTED.indexOf(lang) === -1) lang = DEFAULT_LANG;
    if (persist) {
      try {
        localStorage.setItem(STORAGE_KEY, lang);
      } catch (e) {}
    }
    document.documentElement.setAttribute("lang", lang);
    document.body && document.body.setAttribute("data-ob-lang", lang);
    applyTranslations(lang);
    // Notify any custom listeners
    window.dispatchEvent(new CustomEvent("ob:lang-changed", { detail: { lang: lang } }));
  }

  function getNested(obj, path) {
    var parts = path.split(".");
    var current = obj;
    for (var i = 0; i < parts.length; i++) {
      if (current == null) return undefined;
      current = current[parts[i]];
    }
    return current;
  }

  function applyTranslations(lang) {
    if (!window.__OB_I18N__ || !window.__OB_I18N__[lang]) return;
    var dict = window.__OB_I18N__[lang];

    // Find all elements with data-i18n attribute
    var nodes = document.querySelectorAll("[data-i18n]");
    nodes.forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      var value = getNested(dict, key);
      if (value === undefined) return;

      // Handle data-i18n-attr for non-text attributes (e.g. alt, title, aria-label)
      var attr = el.getAttribute("data-i18n-attr");
      if (attr) {
        el.setAttribute(attr, value);
        return;
      }

      // If element has data-i18n-html, allow HTML; else treat as text
      if (el.hasAttribute("data-i18n-html")) {
        el.innerHTML = value;
      } else {
        el.textContent = value;
      }
    });
  }

  function loadTranslations(callback) {
    if (window.__OB_I18N__) {
      callback(window.__OB_I18N__);
      return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "assets/javascripts/i18n.json", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4) {
        if (xhr.status === 200 || xhr.status === 0) {
          try {
            window.__OB_I18N__ = JSON.parse(xhr.responseText);
            callback(window.__OB_I18N__);
          } catch (err) {
            console.warn("[i18n] Failed to parse translations", err);
          }
        }
      }
    };
    xhr.send();
  }

  // Expose global API
  window.OBi18n = {
    setLanguage: setLanguage,
    set: function (lang) { setLanguage(lang, true); },
    detectLanguage: detectLanguage,
    applyTranslations: applyTranslations,
    getCurrent: function () {
      return document.documentElement.getAttribute("lang") || DEFAULT_LANG;
    }
  };

  // Bootstrap
  function init() {
    var lang = detectLanguage();
    loadTranslations(function () {
      setLanguage(lang, false);

      // Wire the language selector (globe) button if present
      document.addEventListener("click", function (e) {
        var btn = e.target.closest('[data-ob-lang-toggle]');
        if (btn) {
          e.preventDefault();
          var current = window.OBi18n.getCurrent();
          var idx = SUPPORTED.indexOf(current);
          var next = SUPPORTED[(idx + 1) % SUPPORTED.length];
          setLanguage(next, true);
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
