# Sitemap Configuration for ClaimsIQ

## Overview
The sitemap plugin is built into Reflex and automatically generates a `sitemap.xml` file for your application. This helps search engines discover and index your pages.

## Configuration

The SitemapPlugin has been enabled in `rxconfig.py`:

```python
import reflex as rx

config = rx.Config(
    app_name="claimsiq",
    frontend_port=5000,
    backend_port=8001,
    backend_host="0.0.0.0",
    frontend_host="0.0.0.0",
    tailwind={},
    plugins=[
        rx.plugins.SitemapPlugin(),
    ]
)
```

## What It Does

The SitemapPlugin:
- ✅ **Automatically discovers all routes** in your application
- ✅ **Generates sitemap.xml** at `/sitemap.xml`
- ✅ **Updates automatically** when you add new pages
- ✅ **SEO-friendly** format for search engines

## Accessing the Sitemap

Once your app is running, the sitemap is available at:
- **Local Development**: `http://localhost:5000/sitemap.xml`
- **Replit**: `https://your-repl.repl.co/sitemap.xml`
- **Production**: `https://yourdomain.com/sitemap.xml`

## Current Pages in Sitemap

Based on the current app structure, the sitemap includes:
- `/` - Dashboard (main page)

## Adding More Pages

When you add new pages to your app, they'll automatically be included in the sitemap:

```python
# In claimsiq/claimsiq.py
app.add_page(dashboard, route="/", title="ClaimsIQ - Dashboard")
app.add_page(analytics, route="/analytics", title="Analytics")
app.add_page(claims, route="/claims", title="Claims")
```

## Advanced Configuration (Optional)

### Custom Sitemap Metadata

You can add custom metadata to individual pages:

```python
# Add metadata to a specific page
app.add_page(
    dashboard,
    route="/",
    title="ClaimsIQ - Dashboard",
    meta=[
        {"name": "description", "content": "Healthcare claims dashboard"},
        {"property": "og:title", "content": "ClaimsIQ Dashboard"},
    ]
)
```

### Sitemap Priority and Change Frequency

While the basic SitemapPlugin handles most use cases, you can configure priority and change frequency by customizing the plugin (advanced use case):

```python
# Example of advanced sitemap configuration
config = rx.Config(
    plugins=[
        rx.plugins.SitemapPlugin(
            # Custom configuration options can go here
        ),
    ]
)
```

### Excluding Pages from Sitemap

If you need to exclude certain pages from the sitemap, you can mark them accordingly in your routing configuration.

## robots.txt

You may also want to create a `robots.txt` file to guide search engines. Create it in the `assets/` directory:

```
# assets/robots.txt
User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml
```

## Verifying the Sitemap

After deploying:

1. **Test locally**:
   ```bash
   reflex run
   # Visit http://localhost:5000/sitemap.xml
   ```

2. **Test on Replit**:
   - Start the app
   - Visit `https://your-repl.repl.co/sitemap.xml`

3. **Submit to search engines**:
   - Google Search Console: https://search.google.com/search-console
   - Bing Webmaster Tools: https://www.bing.com/webmasters

## Troubleshooting

### Sitemap not generating

**Issue**: `/sitemap.xml` returns 404

**Solutions**:
1. Verify plugin is in `rxconfig.py`:
   ```python
   plugins=[rx.plugins.SitemapPlugin()]
   ```
2. Restart the Reflex app:
   ```bash
   reflex run
   ```
3. Clear the `.web` directory and rebuild:
   ```bash
   rm -rf .web/
   reflex init
   reflex run
   ```

### Sitemap missing pages

**Issue**: Some pages don't appear in sitemap

**Solutions**:
1. Ensure pages are added via `app.add_page()` in `claimsiq.py`
2. Verify routes are properly defined
3. Restart the app to regenerate sitemap

### Sitemap shows wrong URLs

**Issue**: URLs in sitemap.xml are incorrect

**Solutions**:
1. Check `frontend_host` and `frontend_port` in `rxconfig.py`
2. Ensure environment variables are set correctly on Replit
3. Verify the app's public URL matches your domain

## Example Sitemap Output

Your generated `sitemap.xml` will look similar to this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yourdomain.com/</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://yourdomain.com/analytics</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

## SEO Best Practices

1. **Submit your sitemap** to Google Search Console and Bing Webmaster Tools
2. **Keep it updated** - The plugin does this automatically
3. **Monitor crawl errors** in search console
4. **Use descriptive page titles** in `app.add_page()` calls
5. **Add meta descriptions** to improve search results

## References

- [Reflex Plugins Documentation](https://reflex.dev/docs/api-reference/plugins/)
- [Sitemap Protocol](https://www.sitemaps.org/protocol.html)
- [Google Search Console](https://search.google.com/search-console)

## Summary

✅ SitemapPlugin is now **enabled** in `rxconfig.py`
✅ Sitemap will be **auto-generated** at `/sitemap.xml`
✅ All current and future pages are **automatically included**
✅ No additional packages needed - it's **built into Reflex**
