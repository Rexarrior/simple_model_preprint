(function () {
  var STORAGE_KEY = 'theme-preference'
  var COOKIE_NAME = 'theme-preference'
  var preferences = ['auto', 'light', 'dark']
  var systemTheme = window.matchMedia('(prefers-color-scheme: dark)')

  function isPreference(value) { return preferences.indexOf(value) !== -1 }
  function readCookie() {
    var prefix = COOKIE_NAME + '='
    var cookies = document.cookie ? document.cookie.split('; ') : []
    for (var index = 0; index < cookies.length; index += 1) {
      if (cookies[index].indexOf(prefix) === 0) return decodeURIComponent(cookies[index].slice(prefix.length))
    }
    return null
  }
  function readPreference() {
    var cookieValue = readCookie()
    if (isPreference(cookieValue)) return cookieValue
    try {
      var storedValue = window.localStorage.getItem(STORAGE_KEY)
      if (isPreference(storedValue)) return storedValue
    } catch {
      // Cookie persistence remains available when local storage is blocked.
    }
    return 'auto'
  }
  function resolvedTheme(preference) { return preference === 'auto' ? (systemTheme.matches ? 'dark' : 'light') : preference }
  function themeColor(theme) { return theme === 'dark' ? '#0a0a0f' : '#f3f1ea' }
  function applyPreference(preference) {
    var safePreference = isPreference(preference) ? preference : 'auto'
    var theme = resolvedTheme(safePreference)
    var root = document.documentElement
    root.dataset.theme = theme
    root.dataset.themePreference = safePreference
    root.style.colorScheme = theme
    var meta = document.querySelector('meta[name="theme-color"]')
    if (meta) meta.setAttribute('content', themeColor(theme))
    return theme
  }
  function savePreference(preference) {
    try {
      window.localStorage.setItem(STORAGE_KEY, preference)
    } catch {
      // Cookie persistence remains available when local storage is blocked.
    }
    var cookie = COOKIE_NAME + '=' + encodeURIComponent(preference) + '; Path=/; Max-Age=31536000; SameSite=Lax'
    if (location.hostname === 'rexarrior.fun' || location.hostname.endsWith('.rexarrior.fun')) cookie += '; Domain=rexarrior.fun; Secure'
    document.cookie = cookie
  }
  function emitChange(preference, theme) {
    window.dispatchEvent(new CustomEvent('site-theme-change', { detail: { preference: preference, theme: theme } }))
  }
  function setPreference(preference) {
    var safePreference = isPreference(preference) ? preference : 'auto'
    savePreference(safePreference)
    var theme = applyPreference(safePreference)
    emitChange(safePreference, theme)
    return safePreference
  }
  function cyclePreference() {
    var current = readPreference()
    return setPreference(preferences[(preferences.indexOf(current) + 1) % preferences.length])
  }
  window.siteTheme = {
    getPreference: readPreference,
    getResolvedTheme: function () { return resolvedTheme(readPreference()) },
    setPreference: setPreference,
    cyclePreference: cyclePreference,
    preferences: preferences.slice()
  }
  applyPreference(readPreference())
  systemTheme.addEventListener('change', function () {
    var preference = readPreference()
    if (preference !== 'auto') return
    var theme = applyPreference(preference)
    emitChange(preference, theme)
  })
})()
