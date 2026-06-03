import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Daily Medicine Paper Brief",
  description: "Daily medical research briefing MVP",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant">
      <body>
        <div className="shell">
          <header className="topbar">
            <div className="topbar-inner">
              <div className="brand">Daily Medicine Paper Brief</div>
              <nav className="nav" aria-label="Main navigation">
                <a href="/">Today</a>
                <a href="/daily">Daily</a>
                <a href="/articles">Articles</a>
                <a href="/admin/status">Status</a>
                <a href="/admin/setup">Setup</a>
              </nav>
            </div>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
