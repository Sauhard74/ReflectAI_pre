import './globals.css';

export const metadata = {
  title: 'Smart Mirror',
  description: 'AI-powered smart mirror with fashion recommendations'
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}