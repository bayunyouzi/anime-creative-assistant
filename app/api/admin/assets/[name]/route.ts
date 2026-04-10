import { NextResponse } from 'next/server';
import { prisma } from '@/lib/db';
import { verifyToken } from '@/lib/auth';
import { readArchivedImage } from '@/lib/mediaArchive';

const ADMIN_EMAILS = ['1585062016@qq.com'];

export async function GET(
  req: Request,
  { params }: { params: { name: string } }
) {
  try {
    const url = new URL(req.url);
    const queryToken = url.searchParams.get('token');
    const authHeader = req.headers.get('Authorization');
    const headerToken = authHeader?.startsWith('Bearer ') ? authHeader.slice(7) : null;
    const token = queryToken || headerToken;

    if (!token) {
      return NextResponse.json({ error: '未登录' }, { status: 401 });
    }

    const decoded = verifyToken(token);
    if (!decoded?.userId) {
      return NextResponse.json({ error: '登录已失效' }, { status: 401 });
    }

    const me = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: { email: true }
    });
    if (!me || !ADMIN_EMAILS.includes(me.email)) {
      return NextResponse.json({ error: '无管理员权限' }, { status: 403 });
    }

    const archivedImage = await readArchivedImage(params.name);
    if (!archivedImage) {
      return NextResponse.json({ error: '图片不存在' }, { status: 404 });
    }

    return new NextResponse(archivedImage.data, {
      status: 200,
      headers: {
        'Content-Type': archivedImage.mimeType,
        'Cache-Control': 'private, max-age=31536000, immutable'
      }
    });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || 'Internal Server Error' },
      { status: 500 }
    );
  }
}
