import "./globals.css";
import "../sytles/_layout.scss";
import { Metadata } from "next";

export const metadata: Metadata = {
    title: "Runeterra Lore",
    description: "Riot-style lore Explorer for Regions and Champions",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>
                <header>
                    <nav>
                        <a href="/champions">Champions</a>
                        <a href="/regions">Regions</a>
                    </nav>
                </header>
                <main>{children}</main>
            </body>
        </html>
    );
}
