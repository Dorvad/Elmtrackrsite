# Elmtrackr — Verified Product-Facts Registry

**Date reviewed:** 2026-07-16
**Re-verified:** 2026-07-16 against `Dorvad/elmtrackr` `Main` HEAD `df98c3e` — the
same commit this registry was built from. The Android source has **not advanced**
since the previous audit; every fact below was re-checked against source and no
implementation has changed (see "Re-verification" note at the end).
**Product source of truth:** `Dorvad/elmtrackr`, branch `Main` (HEAD `df98c3e`), directory `android/` (read-only).
**Consuming repository:** `Dorvad/Elmtrackrsite` (marketing site).

> Every public claim on the website and in structured data must trace to an
> `implemented` row below. **Do not invent legal, payroll or product claims.**
> Pay results are estimates, never official payroll. Where evidence conflicts,
> both values are recorded (see §Conflicts) rather than the more marketable one.
> Price, Play-listing availability, store rating and review count are **not**
> marked verified — they are not confirmable from the product source.
>
> All source paths are relative to the Android repo root (`android/…`).
> "Changes often?" flags facts that should be re-verified before each site update.

---

## Registry

| # | Product fact | Verified status | Public wording that is safe to use | Important limitation / disclaimer | Android source evidence | Changes often? |
|---|---|---|---|---|---|---|
| 1 | Product name & capitalization | **Implemented** | Use **"ElmTrackr"** (capital E, capital T, one word) — this is the product's own name | Website currently uses "Elmtrackr"/"elmtrackr"; this diverges from the app. Pin one canonical spelling site-wide | `android/app/src/main/res/values/strings.xml:3` (`app_name = "ElmTrackr"`); same in `values-iw/strings.xml:3` and both wear string files; `android/settings.gradle.kts` (`rootProject.name = "ElmTrackr"`) | No |
| 2 | Android package / application ID | **Implemented** | The app's package ID is `com.elmlaunch.myapp` | The Kotlin code namespace `com.elmtrackr.app` is **not** the store ID; do not use it in links. Store ID is permanent | `android/app/build.gradle.kts` (`applicationId = "com.elmlaunch.myapp"`, `namespace = "com.elmtrackr.app"`); confirmed permanent in `android/docs/release-checklist.md` §0 | No |
| 3 | Current app version | **Implemented** | "Version 1.1.0" (only if a version must be shown) | README states an older `1.0.7`/code 9 — stale (see Conflicts). Code is authoritative | `android/app/build.gradle.kts` (`versionName = "1.1.0"`, `versionCode = 10`); wear module matches | **Yes** |
| 4 | Minimum Android version | **Implemented** | "Requires Android 8.0 or newer" | — | `android/app/build.gradle.kts` (`minSdk = 26`) | No |
| 5 | target / compile SDK | **Implemented** | (internal) targets Android 16 (API 36) | CI docs mention API 35 — stale (see Conflicts) | `android/app/build.gradle.kts` (`compileSdk = 36`, `targetSdk = 36`) | Occasionally |
| 6 | Supported Wear OS version | **Implemented** | "Wear OS 3 and newer" | Wear module minSdk 30 | `android/wear/build.gradle.kts` (`minSdk = 30`, `targetSdk = 36`); comment in `android/app/build.gradle.kts` ("targets Wear OS 3, minSdk 30") | No |
| 7 | Play Store URL | **Partially implemented** (URL constructed at runtime; **listing availability unknown**) | If/when the listing is confirmed live: `https://play.google.com/store/apps/details?id=com.elmlaunch.myapp` | **Do not** point the CTA at a listing until it is confirmed public. The site currently links to the generic `play.google.com` | `android/app/src/main/java/com/elmtrackr/app/update/PlayStoreLinks.kt` (builds URL from `context.packageName`); publishing still pending in `android/docs/release-checklist.md` | **Yes** (until live) |
| 8 | Current price | **Unknown — not verifiable from source** | Say nothing specific until confirmed from the live Play listing | No price/currency product string exists in the app; release checklist lists app type as "Free". The site's "$3 once" (EN) and "₪10 once" (HE) are **unverified and mutually inconsistent** | No price string in any `strings*.xml`; `android/docs/release-checklist.md` §6 ("Free"); (site: `index.html`, `he/index.html` on the `legal-pages` branch) | **Yes** |
| 9 | One-time payment vs subscription | **Not implemented** (no billing of any kind) | **Do not claim** any purchase, subscription, one-time payment, or "no subscription" as a product feature | There is **no** Google Play Billing code — no purchases, subscriptions or paywall. Only Play *app-update* is present (not billing) | No `BillingClient`/`ProductDetails`/`INAPP`/`SUBS`/`com.android.billingclient` anywhere in `android/**`; only `play-app-update` in `android/gradle/libs.versions.toml` | No |
| 10 | Clock-in / clock-out methods | **Implemented** (multiple surfaces) | "Clock in and out from the app, a home-screen widget, the notification, an app shortcut, or your watch" | App-lock can gate clock actions from widget/notification/wear when locked | In-app `ui/dashboard/DashboardScreen.kt`; widget `widget/WidgetActions.kt`; notification `notification/ClockOutReceiver.kt`; shortcuts `res/xml/shortcuts.xml` + `shortcuts/ClockOutActions.kt`; wear `wear/…/WearActions.kt`, `wear/…/tile/WearPunchTrampolineActivity` | No |
| 11 | Widgets | **Implemented** (five Glance widgets) | "Home-screen widgets, including 1×1, 4×1 and 4×2 sizes" | Built on Jetpack Glance | `android/app/src/main/java/com/elmtrackr/app/widget/` — `ElmTrackrWidget.kt`, `ElmTrackrMinimalWidget.kt`, `ElmTrackrAuroraWidget.kt`, `ElmTrackrRingWidget.kt`, `ElmTrackrBigActionWidget.kt`; receivers in `AndroidManifest.xml` | No |
| 12 | Wear OS tile & complication | **Implemented** | "Wear OS tile and watch-face complication for one-tap clock-in" | Wear OS 3+ | `android/wear/src/main/java/com/elmtrackr/wear/tile/ElmTrackrTileService.kt`; `wear/…/complication/ElmTrackrComplicationService.kt`; registered in `wear/…/AndroidManifest.xml` | No |
| 13 | Estimated gross pay | **Implemented** (explicitly an estimate) | "See an estimated gross as you work" — always the word **estimate** | Must keep the disclaimer: *"Estimated only. Actual pay may vary… not legal, tax, payroll, accounting, or financial advice."* | `domain/PayrollCalculator.kt`; `domain/compensation/CompensationResolver.kt:203-205` (`COMPENSATION_ESTIMATE_NOTE`); UI `ui/shifts/ShiftEditFormUi.kt:604` | No |
| 14 | Daily & weekly overtime | **Implemented** | "Daily and weekly overtime, by your own thresholds" | Tiers are user-configurable per region | `domain/PayrollCalculator.kt`; `domain/compensation/RegionPresets.kt` (`dailyOvertimeTiers`, `weeklyOvertimeTiers`) | No |
| 15 | Premium profiles & stacking | **Implemented** | "Premium profiles for weekend, night and holiday rates, with configurable stacking" | Six stacking modes; default profile "Premium" ×1.5 | `domain/premium/PremiumStacking.kt`; `PremiumType`/`StackingPolicy` (six values) per `android/docs/supabase-contract.md` | No |
| 16 | Regional presets | **Implemented** (six) | "Regional presets for the US, California, UK, EU and Israel, plus fully custom rules" | Presets encode region specifics (e.g. IL Fri+Sat weekend, night 22:00–06:00) | `domain/compensation/RegionPresets.kt` (`RegionCode.US`, `US_CA`, `GB`, `EU`, `IL`, `CUSTOM`) | Occasionally |
| 17 | Task tracking & suggestions | **Implemented** | "Track tasks per shift, with smart suggestions" | Task snapshots stored on the shift at clock-in | `data/local/entity/TaskEntity.kt`, `domain/model/Task.kt`, `data/local/dao/TaskDao.kt`; suggestions `domain/tasks/TaskHabitSuggestionBuilder.kt`, `TaskDefaultRulesBuilder.kt`; UI `ui/tasks/TaskSelectorBar.kt` | No |
| 18 | Reports | **Implemented** | "Monthly and weekly reports with regular/overtime/weekend breakdowns and trends" | Built entirely from local data; some insights are feature-gated | `domain/MonthlyReportBuilder`, `WeeklyBreakdownBuilder`, `TaskMonthlyReportBuilder`; UI `ui/reports/ReportsScreen.kt`, `ReportsViewModel.kt` | No |
| 19 | CSV & PDF export | **Implemented** (native) | "Export your shifts as CSV or PDF" | PDF uses Android's native `PdfDocument` (no external lib); CSV filename `elmtrackr-YYYY-MM.csv` | `ui/reports/ReportExporter.kt` (`android.graphics.pdf.PdfDocument`; `shareShiftPdf`, `shareRefundPdf`; CSV via `ACTION_SEND`) | No |
| 20 | Receipt capture & OCR | **Implemented** (CameraX + ML Kit + Tesseract all invoked) | "Capture receipts and read them on-device with OCR" | On-device; used within the refunds flow | CameraX in `ui/refunds/`; `ui/refunds/DocumentScannerLauncher.kt` (ML Kit doc scanner); `data/receipt/MLKitReceiptTextRecognizer.kt` (`TextRecognition`); `data/receipt/TesseractHebrewTextRecognizer.kt` (`TessBaseAPI`) | No |
| 21 | Supported OCR languages | **Implemented** (Hebrew + Latin-script only) | "On-device OCR for Latin-script text and Hebrew" | **Do not** claim broad multi-language OCR. Only `heb.traineddata` is bundled; ML Kit is the Latin recognizer | ML Kit `TextRecognizerOptions.DEFAULT_OPTIONS` (`MLKitReceiptTextRecognizer.kt`); Hebrew `data/receipt/TesseractHebrewTextRecognizer.kt` (`LANGUAGE = "heb"`) + `app/src/main/assets/tessdata/heb.traineddata` | No |
| 22 | Reimbursement / refund workflow | **Implemented** (feature-gated) | "Track commute-refund claims and export a reimbursement packet" | Gated by the `featuresTravelRefunds` setting; providers Lime/Dott/Bird/Taxi/Other | `refund_claims` table + `RefundAction` enum (`docs/supabase-contract.md`); UI `ui/refunds/RefundClaimViewModel.kt`; reimbursement PDF in `ReportExporter.kt` | No |
| 23 | Local storage | **Implemented** (Room / SQLite, source of truth) | "Your data lives on your device" | DB file `elmtrackr.db`; receipt images stored locally | `data/local/ElmTrackrDatabase.kt` (Room, 13 migrations); receipts `data/receipts/PhotoFileManager` | No |
| 24 | Cloud synchronization | **Implemented** — **optional** | "Optional cloud sync across devices" | Works only when Supabase keys are configured **and** the user signs in; otherwise fully local. Sync needs a network | `data/sync/SyncRepositoryImpl.kt`, `SyncWorker`, `SyncScheduler`; `SupabaseClientProvider.get()` returns `null` when unconfigured (`SyncResult.NotConfigured`) | Occasionally |
| 25 | Authentication | **Implemented** — email/password only, optional | "Optional account with email and password" | **Do not** claim Google/social or anonymous sign-in — none exists. App runs fully without an account | `data/repository/SupabaseAuthRepository.kt` (Supabase `Email` provider only); deep links `elmtrackr://auth/callback`, `…/reset-password` | No |
| 26 | Database encryption | **Implemented** (SQLCipher) | "Your on-device database is encrypted" | Passphrase generated/stored on device; one-time migration from any legacy plaintext DB | `data/local/ElmTrackrDatabase.kt:27,89` (`SupportOpenHelperFactory`, `System.loadLibrary("sqlcipher")`); `data/local/PlaintextDatabaseMigrator.kt` | No |
| 27 | Biometric app lock | **Implemented** | "Lock the app with biometrics or your device credential" | Uses `BIOMETRIC_STRONG or DEVICE_CREDENTIAL`; guards remote clock actions when locked | `security/BiometricAuthPrompt.kt`, `security/AppLockController.kt`, `ui/security/AppLockGate.kt` | No |
| 28 | Crash diagnostics | **Implemented** (Sentry, opt-out, double-gated) | "Optional crash reporting you can turn off" | Off unless a DSN is compiled in **and** the user consents (default on); `isSendDefaultPii = false` | `monitoring/CrashReporting.kt` (`SentryAndroid`, `BuildConfig.SENTRY_DSN`, `isEnabledByUser`); opt-out "Settings → Help & About → Share crash reports" | No |
| 29 | Account & data deletion | **Implemented** (in-app) | "Delete your account and data from within the app" | In-app deletion via `delete_own_account` RPC. Play also requires a **web** deletion URL — that page is **not in this repo (unknown)** | `SupabaseAuthRepository.kt:193` (`rpc("delete_own_account")`); scope in `docs/supabase-contract.md`; UI `ui/settings/SettingsDetailScreens.kt` | No |
| 30 | Hebrew localization | **Implemented** — near-complete (not literal 100%) | "Full Hebrew support" | Avoid claiming literal 100% parity: 6 widget-preview strings are untranslated (see Conflicts) | `android/app/src/main/res/values-iw/` (16 string files + `arrays.xml`); ~1081 (iw) vs ~1087 (en) | Occasionally |
| 31 | Offline behavior | **Implemented** (offline-first) | "Works fully offline; sync when you're back online" | Requires network only for sync, auth, receipt upload/retrieval and in-app updates. OCR is on-device | README "Offline-first sync"; Room-first writes with `PENDING_*` status; `data/sync/*` | No |
| 32 | Notification & reminder rules | **Implemented** | "A live clocked-in notification and overtime reminders" | Feature-gated (`features_overtime_reminders`, default on); needs `POST_NOTIFICATIONS` on Android 13+; app works if denied | `notification/` + `ActiveShiftNotificationManager`; `LongShiftReminderWorker`; channels `active_shift`, `reminders`; strings `notif_overtime_*` | No |
| 33 | Supported platforms (summary) | **Implemented** | "Android 8.0+ phones and Wear OS 3+ watches" | Both modules share `applicationId com.elmlaunch.myapp`; watch app ships as a separate artifact in the same listing | `android/app/build.gradle.kts` (minSdk 26); `android/wear/build.gradle.kts` (minSdk 30) | No |

---

## Conflicts (recorded, not resolved)

1. **App version.** Code = `1.1.0` / `versionCode 10` (`android/app/build.gradle.kts`); `android/README.md` (Play upload section) says `1.0.7` / code 9. **Code is authoritative.**
2. **Price (cross-repo).** Website English = "$3 once" (`index.html`); website Hebrew (undeployed `legal-pages` branch) = "₪10 once" (`he/index.html`). The Android source has **no price** and no billing code (listing intent "Free"). All price claims are unverified and internally inconsistent — **remove or confirm from the live Play listing before publishing any price.**
3. **Brand capitalization.** Product source = **"ElmTrackr"** (all string resources). Website mixes "Elmtrackr" (title/meta), "elmtrackr" (wordmark) and "ElmTrackr" (widget mockups, legal pages).
4. **Hebrew string parity.** Docs claim "full parity, 1,027/1,027" (`android/README.md`, `android/docs/release-checklist.md`). Actual: ~1087 (en) vs ~1081 (iw); 6 untranslated `strings_widgets.xml` keys (`widget_preview_brand`, `widget_preview_goal_sub`, `widget_preview_percent`, `widget_preview_time`, `widget_preview_time_idle`, `widget_preview_today_sub`).
5. **Native clock styles.** `android/README.md` says "only three render natively"; code `ui/dashboard/SupportedClockStyle.kt` renders **16** natively and `docs/supabase-contract.md` agrees "all persisted styles render natively." Code is authoritative. (Not a website claim today, but noted.)
6. **CI platform SDK.** `android/README.md` GitHub Actions section says platform/build-tools **35**; build files use **36**.

---

## Unresolved facts requiring manual confirmation

- **Play Store listing availability** — is `com.elmlaunch.myapp` actually published and public? (Not verifiable from source; publishing steps still pending in the release checklist.)
- **Current price** — the real price/monetization on the live listing (source says none; site claims differ).
- **Store rating & review count** — not verifiable from any authoritative source; do not publish.
- **Web account-deletion URL** — required by Play's data-safety form; the page is not in the Android repo. Confirm where it is hosted (candidate: this marketing site).
- **Canonical brand spelling decision** — "ElmTrackr" per the app; confirm the owner wants the website aligned to it.

---

## Re-verification (2026-07-16)

The Android app repo (`Dorvad/elmtrackr`) was re-cloned and its `Main` branch
HEAD is `df98c3e` — identical to the commit this registry was originally built
from. Because the source is byte-for-byte the same commit, **no implemented
behavior has changed** and no fact row required a value update. Each of the
following was re-checked directly against source at this HEAD and matches the
registry:

| Area | Re-checked value | Source |
|---|---|---|
| Version | `versionName 1.1.0`, `versionCode 10` | `android/app/build.gradle.kts` |
| Min Android / SDKs | `minSdk 26`, `targetSdk 36`, `compileSdk 36` | `android/app/build.gradle.kts` |
| Wear OS | `minSdk 30`, `targetSdk 36` | `android/wear/build.gradle.kts` |
| Play listing status | still unverifiable from source (publishing pending) | release checklist |
| Application ID | `com.elmlaunch.myapp` | `android/app/build.gradle.kts` |
| Price / billing | no price string; no `BillingClient` present | `strings*.xml`, `android/**` |
| Widgets | 5 Glance widgets (`ElmTrackrWidget`, `Minimal`, `Aurora`, `Ring`, `BigAction`) | `…/widget/` |
| Tile & complication | `ElmTrackrTileService`, `ElmTrackrComplicationService` | `…/wear/tile`, `…/wear/complication` |
| OCR | ML Kit (Latin) + Tesseract `heb.traineddata` (Hebrew), on device | `…/data/receipt/`, `assets/tessdata/` |
| Receipt sync | receipts stored locally; sync only when Supabase configured + signed in | `data/sync/*`, `PhotoFileManager` |
| Regional presets | 6: `US`, `US_CA`, `GB`, `EU`, `IL`, `CUSTOM` | `RegionPresets.kt` |
| Overtime | daily & weekly, user thresholds | `PayrollCalculator.kt`, `RegionPresets.kt` |
| Encryption | SQLCipher `SupportOpenHelperFactory` / `loadLibrary("sqlcipher")` (at rest) | `ElmTrackrDatabase.kt:27,86,89` |
| Biometric lock | `BiometricAuthPrompt`, `AppLockController` | `…/security/` |
| Sentry | DSN-gated, `isSendDefaultPii = false`, opt-out | `monitoring/CrashReporting.kt` |
| Cloud sync | optional; `SyncResult.NotConfigured` when unset | `data/sync/SyncRepositoryImpl.kt` |
| Account deletion | `rpc("delete_own_account")` in-app | `SupabaseAuthRepository.kt:193` |
| Hebrew localization | ~1087 (en) vs ~1081 (iw) strings — near-complete, not literal 100% | `values/`, `values-iw/` |

The only edit made during re-verification was correcting the deletion-RPC line
citation (189 → 193). All open items in "Unresolved facts requiring manual
confirmation" remain open — none is resolvable from source.
