import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "MergePDF — Free PDF Merger for Windows",
  description:
    "Merge multiple PDFs into one in seconds. Free, offline, no uploads. Download the Windows app.",
};

const GITHUB_RELEASE_URL = "https://github.com/BagelSamurai/mergepdf";

const FEATURES = [
  {
    icon: "⚡",
    title: "Instant merging",
    desc: "Combine dozens of PDFs in seconds, no matter the file size.",
  },
  {
    icon: "🔒",
    title: "100% offline",
    desc: "Your files never leave your computer. No uploads, no cloud, no tracking.",
  },
  {
    icon: "🗂️",
    title: "Drag & reorder",
    desc: "Add files in any order and rearrange them before merging.",
  },
  {
    icon: "🌙",
    title: "Light & dark mode",
    desc: "Follows your system theme automatically.",
  },
  {
    icon: "🆓",
    title: "Completely free",
    desc: "No trial, no watermarks, no account required. Ever.",
  },
  {
    icon: "📄",
    title: "Page count preview",
    desc: "See how many pages each PDF has before you merge.",
  },
];

const STEPS = [
  { n: "1", text: "Download and open MergePDF" },
  { n: "2", text: "Drag in your PDF files" },
  { n: "3", text: "Reorder them if needed" },
  { n: "4", text: "Hit Merge — done" },
];

export default function Home() {
  return (
    <div className="min-h-screen bg-white text-slate-900 font-sans">
      {/* ── Nav ── */}
      <nav
        className="fixed top-0 inset-x-0 z-50 bg-white/80 backdrop-blur
                      border-b border-slate-100"
      >
        <div className="max-w-5xl mx-auto px-6 h-14 flex items-center justify-between">
          <span className="font-bold text-lg tracking-tight">
            Merge<span className="text-blue-600">PDF</span>
          </span>

          <a
            href={GITHUB_RELEASE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm font-medium bg-blue-600 text-white
                       px-4 py-1.5 rounded-full hover:bg-blue-700 transition-colors"
          >
            Download free
          </a>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="pt-40 pb-24 px-6 text-center">
        <div className="max-w-3xl mx-auto">
          <div
            className="inline-block bg-blue-50 text-blue-700 text-xs font-semibold
                           px-3 py-1 rounded-full mb-6 tracking-wide uppercase"
          >
            Free · Offline · Windows
          </div>
          <h1 className="text-5xl sm:text-6xl font-bold tracking-tight leading-tight mb-6">
            Merge PDFs in <span className="text-blue-600">seconds</span>
          </h1>
          <p className="text-lg text-slate-500 max-w-xl mx-auto mb-10">
            A fast, private desktop app for Windows. Drag in your PDFs, reorder
            them, and merge — no internet required.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <a
              href={GITHUB_RELEASE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2
                         bg-blue-600 text-white font-semibold px-8 py-3.5
                         rounded-xl hover:bg-blue-700 transition-colors text-sm"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                strokeWidth={2.5}
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2
                           M7 10l5 5 5-5M12 15V3"
                />
              </svg>
              Download for Windows
            </a>

            <a
              href={GITHUB_RELEASE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2
                         border border-slate-200 text-slate-700 font-medium
                         px-8 py-3.5 rounded-xl hover:bg-slate-50
                         transition-colors text-sm"
            >
              View on GitHub
            </a>
          </div>
          <p className="text-xs text-slate-400 mt-4">
            Free download · No installer required · Windows 10/11
          </p>
        </div>
      </section>

      {/* ── App screenshot placeholder ── */}
      <section className="pb-24 px-6">
        <div
          className="max-w-2xl mx-auto bg-slate-50 border border-slate-200
                        rounded-2xl h-80 flex items-center justify-center"
        >
          <div className="text-center">
            <div className="text-5xl mb-3">🖥️</div>
            <p className="text-slate-400 text-sm">App screenshot</p>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="py-24 px-6 bg-slate-50">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-3">
            Everything you need, nothing you don&apos;t
          </h2>
          <p className="text-slate-500 text-center mb-14 max-w-md mx-auto">
            Built to be fast and simple. Open it, merge, close it.
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f) => (
              <div
                key={f.title}
                className="bg-white border border-slate-200 rounded-2xl p-6"
              >
                <div className="text-3xl mb-4">{f.icon}</div>
                <h3 className="font-semibold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-sm text-slate-500 leading-relaxed">
                  {f.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── How it works ── */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-14">How it works</h2>
          <div className="flex flex-col gap-4">
            {STEPS.map((s) => (
              <div
                key={s.n}
                className="flex items-center gap-5 bg-slate-50
                            border border-slate-200 rounded-2xl px-6 py-5"
              >
                <span
                  className="w-9 h-9 rounded-full bg-blue-600 text-white
                                 font-bold text-sm flex items-center justify-center
                                 shrink-0"
                >
                  {s.n}
                </span>
                <span className="text-slate-700 font-medium">{s.text}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-24 px-6 bg-blue-600 text-white text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">Ready to merge your PDFs?</h2>
          <p className="text-blue-100 mb-8">
            Free download. No account. Works offline.
          </p>

          <a
            href={GITHUB_RELEASE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 bg-white text-blue-600
                       font-semibold px-8 py-3.5 rounded-xl
                       hover:bg-blue-50 transition-colors text-sm"
          >
            Download MergePDF free
          </a>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="py-10 px-6 border-t border-slate-100 text-center">
        <p className="text-sm text-slate-400">
          MergePDF · Free &amp; open source ·{" "}
          <a
            href={GITHUB_RELEASE_URL}
            className="hover:text-slate-600 transition-colors"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}
