import { mkdir, readdir, readFile, stat, unlink, writeFile } from 'fs/promises';
import path from 'path';
import { randomUUID } from 'crypto';

export const ADMIN_ARCHIVE_ROUTE_PREFIX = '/api/admin/assets/';

const DEFAULT_ARCHIVE_DIR = path.join(process.cwd(), 'public', 'admin-generated-images');
const ADMIN_ARCHIVE_DIR = process.env.ADMIN_IMAGE_ARCHIVE_DIR || DEFAULT_ARCHIVE_DIR;

const normalizeImageRef = (value: string | null | undefined) =>
  String(value || '').trim().replace(/[`"'“”‘’]/g, '').trim();

const ensureArchiveDir = async () => {
  await mkdir(ADMIN_ARCHIVE_DIR, { recursive: true });
  return ADMIN_ARCHIVE_DIR;
};

const extensionFromMime = (mimeType?: string | null) => {
  const normalized = String(mimeType || '').toLowerCase();
  if (normalized.includes('png')) return '.png';
  if (normalized.includes('webp')) return '.webp';
  if (normalized.includes('gif')) return '.gif';
  return '.jpg';
};

const extensionFromUrl = (url: string) => {
  try {
    const pathname = new URL(url).pathname.toLowerCase();
    const ext = path.extname(pathname);
    if (ext && ext.length <= 6) return ext;
  } catch {}
  return '';
};

const getImageBufferFromRef = async (raw: string) => {
  if (raw.startsWith('data:image/')) {
    const match = raw.match(/^data:(image\/[a-zA-Z0-9.+-]+);base64,(.+)$/);
    if (!match) return null;
    const [, mimeType, base64Data] = match;
    return {
      buffer: Buffer.from(base64Data, 'base64'),
      mimeType
    };
  }

  if (!/^https?:\/\//i.test(raw)) return null;
  const response = await fetch(raw);
  if (!response.ok) return null;
  return {
    buffer: Buffer.from(await response.arrayBuffer()),
    mimeType: response.headers.get('content-type') || 'image/jpeg'
  };
};

export const archiveImageForAdmin = async (imageRef: string | null | undefined) => {
  const raw = normalizeImageRef(imageRef);
  if (!raw) return null;
  if (raw.startsWith(ADMIN_ARCHIVE_ROUTE_PREFIX)) return raw;

  const imageData = await getImageBufferFromRef(raw);
  if (!imageData) return null;

  const archiveDir = await ensureArchiveDir();
  const ext = extensionFromUrl(raw) || extensionFromMime(imageData.mimeType);
  const fileName = `${Date.now()}-${randomUUID()}${ext}`;
  const filePath = path.join(archiveDir, fileName);
  await writeFile(filePath, imageData.buffer);
  return `${ADMIN_ARCHIVE_ROUTE_PREFIX}${fileName}`;
};

export const extractArchiveFileName = (archiveUrl: string | null | undefined) => {
  const raw = normalizeImageRef(archiveUrl);
  if (!raw.startsWith(ADMIN_ARCHIVE_ROUTE_PREFIX)) return null;
  const fileName = raw.slice(ADMIN_ARCHIVE_ROUTE_PREFIX.length);
  if (!fileName || fileName.includes('/') || fileName.includes('\\')) return null;
  return fileName;
};

export const deleteArchivedImage = async (archiveUrl: string | null | undefined) => {
  const fileName = extractArchiveFileName(archiveUrl);
  if (!fileName) return;
  const filePath = path.join(ADMIN_ARCHIVE_DIR, fileName);
  await unlink(filePath).catch(() => {});
};

export const readArchivedImage = async (fileName: string) => {
  const safeName = path.basename(fileName);
  if (!safeName || safeName !== fileName) return null;
  const filePath = path.join(ADMIN_ARCHIVE_DIR, safeName);
  const fileStat = await stat(filePath).catch(() => null);
  if (!fileStat?.isFile()) return null;
  const data = await readFile(filePath);
  const ext = path.extname(safeName).toLowerCase();
  const mimeType =
    ext === '.png' ? 'image/png' :
    ext === '.webp' ? 'image/webp' :
    ext === '.gif' ? 'image/gif' :
    'image/jpeg';
  return { data, mimeType };
};

export const trimArchiveFiles = async (keepCount: number) => {
  const archiveDir = await ensureArchiveDir();
  const entries = await readdir(archiveDir).catch(() => []);
  const withStat = await Promise.all(
    entries.map(async (name) => {
      const filePath = path.join(archiveDir, name);
      const fileStat = await stat(filePath).catch(() => null);
      return fileStat?.isFile() ? { name, filePath, mtimeMs: fileStat.mtimeMs } : null;
    })
  );

  const files = withStat
    .filter((item): item is { name: string; filePath: string; mtimeMs: number } => Boolean(item))
    .sort((a, b) => b.mtimeMs - a.mtimeMs);

  const staleFiles = files.slice(keepCount);
  await Promise.all(staleFiles.map((file) => unlink(file.filePath).catch(() => {})));
  return staleFiles.map((file) => `${ADMIN_ARCHIVE_ROUTE_PREFIX}${file.name}`);
};
