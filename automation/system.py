#!/usr/bin/env python3
"""
🤖 LINETOGEL FULL AUTOMATED SEO SYSTEM
Auto-generate sitemap, schema, freshness, internal links
Run: python3 automation/system.py
"""

import os, re, glob, json, hashlib
from datetime import date, datetime
from collections import defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()

# ═══════════════════════════════════════════
# MODULE 1: Auto Sitemap Generator
# ═══════════════════════════════════════════
def generate_sitemap():
    """Scan all HTML files and generate sitemap.xml"""
    urls = []
    
    for fp in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
        rel = os.path.relpath(fp, BASE)
        if 'google76be2f736f9cf7c4' in rel:
            continue
        
        url = f'https://linetogel-pi.vercel.app/{rel}'
        
        # Determine priority based on path
        if rel == 'index.html':
            priority, changefreq = '1.0', 'daily'
        elif 'pages/' in rel:
            priority, changefreq = '0.9', 'weekly'
        elif 'artikel/' in rel:
            priority, changefreq = '0.7', 'weekly'
        elif 'lokasi/' in rel:
            priority, changefreq = '0.7', 'weekly'
        else:
            priority, changefreq = '0.6', 'monthly'
        
        urls.append({
            'loc': url,
            'lastmod': TODAY,
            'changefreq': changefreq,
            'priority': priority
        })
    
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for u in sorted(urls, key=lambda x: (-float(x['priority']), x['loc'])):
        sitemap += f'  <url>\n'
        sitemap += f'    <loc>{u["loc"]}</loc>\n'
        sitemap += f'    <lastmod>{u["lastmod"]}</lastmod>\n'
        sitemap += f'    <changefreq>{u["changefreq"]}</changefreq>\n'
        sitemap += f'    <priority>{u["priority"]}</priority>\n'
        sitemap += f'  </url>\n'
    
    sitemap += '</urlset>\n'
    
    with open(f'{BASE}/sitemap.xml', 'w') as f:
        f.write(sitemap)
    
    return len(urls)

# ═══════════════════════════════════════════
# MODULE 2: Content Freshness Auto-Updater
# ═══════════════════════════════════════════
def update_freshness():
    """Update all datePublished/dateModified and visible dates"""
    updated = 0
    
    for fp in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
        try:
            with open(fp, 'r') as f:
                content = f.read()
            
            original = content
            
            # Update JSON-LD dates
            content = re.sub(
                r'"datePublished":\s*"[^"]*"',
                f'"datePublished": "{TODAY}"',
                content
            )
            content = re.sub(
                r'"dateModified":\s*"[^"]*"',
                f'"dateModified": "{TODAY}"',
                content
            )
            
            # Update visible dates
            content = re.sub(
                r'📅 Diperbarui:\s*[^<]+',
                f'📅 Diperbarui: {TODAY}',
                content
            )
            
            # Update sitemap lastmod
            content = re.sub(
                r'<lastmod>[^<]+</lastmod>',
                f'<lastmod>{TODAY}</lastmod>',
                content
            )
            
            if content != original:
                with open(fp, 'w') as f:
                    f.write(content)
                updated += 1
        except Exception as e:
            print(f"  ⚠️ Error updating {fp}: {e}")
    
    return updated

# ═══════════════════════════════════════════
# MODULE 3: Internal Link Optimizer
# ═══════════════════════════════════════════
SILO_MAP = {
    'pasaran': {
        'pillar': '/pages/pasaran.html',
        'subs': [
            '/artikel/pasaran-toto-terlengkap-2026.html',
            '/artikel/jam-result-pasaran-toto.html',
            '/artikel/daftar-pasaran-toto-terlengkap.html',
        ]
    },
    'panduan': {
        'pillar': '/artikel/panduan-lengkap-toto-4d.html',
        'subs': [
            '/artikel/panduan-lengkap-toto-online.html',
            '/artikel/cara-daftar-akun-toto.html',
            '/artikel/cara-deposit-murah-toto.html',
            '/artikel/cara-withdraw-cepat-toto.html',
            '/artikel/toto-mobile-android-iphone.html',
            '/artikel/faq-toto-online.html',
        ]
    },
    'strategi': {
        'pillar': '/artikel/strategi-menang-toto-2026.html',
        'subs': [
            '/artikel/strategi-4d-3d-2d.html',
            '/artikel/rumus-analisis-angka-toto.html',
            '/artikel/manajemen-modal-toto.html',
            '/artikel/cara-membaca-statistik-toto.html',
        ]
    },
    'kepercayaan': {
        'pillar': '/artikel/situs-toto-terpercaya-2026-guide.html',
        'subs': [
            '/artikel/situs-toto-terpercaya-2026.html',
            '/artikel/tips-menghindari-penipuan-toto.html',
            '/artikel/keamanan-transaksi-toto.html',
            '/artikel/perbandingan-situs-toto.html',
            '/artikel/testimoni-member-toto.html',
        ]
    },
    'bonus': {
        'pillar': '/artikel/deposit-withdraw-toto-panduan.html',
        'subs': [
            '/artikel/bonus-deposit-member-baru.html',
            '/artikel/promo-bonus-toto-terbaru.html',
            '/artikel/program-referral-toto.html',
            '/artikel/event-mingguan-toto.html',
        ]
    }
}

def analyze_internal_links():
    """Analyze internal linking structure and suggest improvements"""
    pages = {}
    
    for fp in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
        rel = '/' + os.path.relpath(fp, BASE)
        
        with open(fp, 'r') as f:
            content = f.read()
        
        outgoing = re.findall(r'href="(/[^"]*)"', content)
        outgoing = [l for l in outgoing if l.startswith('/') and '.html' in l]
        
        pages[rel] = {
            'file': fp,
            'outgoing': outgoing,
            'incoming': []
        }
    
    # Build incoming links
    for page, data in pages.items():
        for out_link in data['outgoing']:
            if out_link in pages:
                pages[out_link]['incoming'].append(page)
    
    # Report orphan pages (no incoming links)
    orphans = []
    weak = []
    
    for page, data in pages.items():
        incoming_count = len(data['incoming'])
        outgoing_count = len(data['outgoing'])
        
        if incoming_count == 0 and page != '/index.html':
            orphans.append(page)
        
        if incoming_count < 2 and page != '/index.html':
            weak.append((page, incoming_count, outgoing_count))
    
    report = {
        'total_pages': len(pages),
        'orphans': orphans,
        'weak_links': weak,
        'pages': pages
    }
    
    return report

# ═══════════════════════════════════════════
# MODULE 4: Schema Completeness Checker
# ═══════════════════════════════════════════
REQUIRED_SCHEMAS = {
    'index.html': ['WebSite', 'Organization', 'FAQPage', 'BreadcrumbList', 'LocalBusiness'],
    'artikel/': ['Article', 'BreadcrumbList'],
    'lokasi/': ['LocalBusiness', 'BreadcrumbList', 'FAQPage'],
    'pages/': ['BreadcrumbList'],
}

def check_schema_completeness():
    """Check all pages have required schemas"""
    results = []
    
    for fp in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
        rel = os.path.relpath(fp, BASE)
        
        with open(fp, 'r') as f:
            content = f.read()
        
        schemas = set(re.findall(r'"@type":\s*"(\w+)"', content))
        
        # Determine required schemas
        required = set()
        for prefix, req in REQUIRED_SCHEMAS.items():
            if rel.startswith(prefix):
                required = set(req)
                break
        
        missing = required - schemas
        extra = schemas - required
        
        if missing:
            results.append({
                'page': rel,
                'status': '⚠️ MISSING',
                'missing': list(missing),
                'present': list(schemas)
            })
        else:
            results.append({
                'page': rel,
                'status': '✅ COMPLETE',
                'present': list(schemas)
            })
    
    return results

# ═══════════════════════════════════════════
# MODULE 5: Content Quality Scorer
# ═══════════════════════════════════════════
def score_content():
    """Score all pages on content quality"""
    scores = []
    
    for fp in sorted(glob.glob(f'{BASE}/**/*.html', recursive=True)):
        rel = os.path.relpath(fp, BASE)
        
        with open(fp, 'r') as f:
            content = f.read()
        
        score = 100
        
        # Word count
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'\s+', ' ', text).strip()
        word_count = len(text.split())
        
        if word_count < 300: score -= 20
        elif word_count < 600: score -= 10
        elif word_count < 1000: score -= 5
        elif word_count > 1500: score += 5
        elif word_count > 2500: score += 10
        
        # H1 check
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        if h1_count == 0: score -= 15
        if h1_count > 1: score -= 5
        
        # H2 check
        h2_count = len(re.findall(r'<h2[^>]*>', content))
        if h2_count < 2: score -= 10
        
        # Images
        img_count = len(re.findall(r'<img[^>]+src="[^"]*"', content))
        if 'artikel/' in rel and img_count < 2: score -= 5
        
        # Internal links
        internal = len(re.findall(r'href="(/[^"]*\.html)"', content))
        if internal < 3: score -= 5
        
        # Schema
        schema_count = content.count('"@type"')
        if schema_count < 2: score -= 10
        elif schema_count >= 5: score += 5
        
        scores.append({
            'page': rel,
            'score': max(0, min(100, score)),
            'words': word_count,
            'h1': h1_count,
            'h2': h2_count,
            'images': img_count,
            'internal_links': internal,
            'schemas': schema_count
        })
    
    return scores

# ═══════════════════════════════════════════
# MAIN: Run All Modules
# ═══════════════════════════════════════════
if __name__ == '__main__':
    print("🤖 LINETOGEL AUTO-SEO SYSTEM v1.0")
    print(f"📅 {TODAY}")
    print("=" * 60)
    
    # 1. Sitemap
    print("\n📊 Generating sitemap...")
    count = generate_sitemap()
    print(f"   ✅ {count} URLs in sitemap.xml")
    
    # 2. Freshness
    print("\n🔄 Updating content freshness...")
    updated = update_freshness()
    print(f"   ✅ {updated} pages refreshed")
    
    # 3. Internal linking
    print("\n🔗 Analyzing internal links...")
    report = analyze_internal_links()
    print(f"   📄 {report['total_pages']} pages analyzed")
    if report['orphans']:
        print(f"   ⚠️ {len(report['orphans'])} orphan pages (no incoming links):")
        for o in report['orphans'][:5]:
            print(f"      {o}")
    
    # 4. Schema check
    print("\n🏗️ Checking schema completeness...")
    schema_results = check_schema_completeness()
    missing_count = len([s for s in schema_results if s['status'].startswith('⚠️')])
    print(f"   ✅ {len(schema_results) - missing_count} pages complete")
    if missing_count:
        print(f"   ⚠️ {missing_count} pages missing schemas")
    
    # 5. Content quality
    print("\n📝 Scoring content quality...")
    quality = score_content()
    avg = sum(q['score'] for q in quality) / len(quality) if quality else 0
    low = [q for q in quality if q['score'] < 70]
    print(f"   📊 Average score: {avg:.1f}/100")
    if low:
        print(f"   ⚠️ {len(low)} pages below 70:")
        for l in low:
            print(f"      {l['page']}: {l['score']} ({l['words']} words)")
    
    print("\n" + "=" * 60)
    print("🎉 AUTO-SEO SYSTEM COMPLETE")
    print("=" * 60)
