import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex justify-between items-center px-8 py-4 border-b border-brand-border">
      <h1 className="text-xl font-bold text-brand-primary">InsightFlow</h1>

      <div className="flex gap-4">
        <Link href="/login" className="text-brand-muted hover:text-white">
          Login
        </Link>

        <Link
          href="/register"
          className="bg-brand-primary px-4 py-2 rounded-md text-white hover:opacity-90"
        >
          Criar conta
        </Link>
      </div>
    </nav>
  );
}