import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { jwtDecode } from 'jwt-decode';

export function middleware(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  if (request.nextUrl.pathname.startsWith('/dashboard') && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (token) {
    const decoded: any = jwtDecode(token);
    const role = decoded.role;

    // Se for rota de admin e o cara não for admin, chuta ele pro dashboard
    if (request.nextUrl.pathname.startsWith('/admin') && role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard', request.url));
    }
  }

  return NextResponse.next();
}
