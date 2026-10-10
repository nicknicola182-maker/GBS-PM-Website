# 09_DIGITAL/social - social media assets (v1.0)

Rendered by `node tools/render.mjs tools/manifests/09_digital.json` from the HTML sources here (screenshot jobs at 1x, exact pixel sizes). Edit the HTML, not the PNGs. Sources link the brand tokens and fonts; the web address is the `{{company.domain}}` token.

| Asset | Source | Output | Size | Notes |
|---|---|---|---|---|
| LinkedIn company banner | `linkedin-banner.html` | `GBS_HORIZON_SOCIAL_LINKEDIN-BANNER_1584x396_v1.0.png` | 1584 x 396 | Off-white ground, no-strap primary logo left, headline "Specialist maintenance for managed property", sage strapline band with red pipes and web address. LinkedIn crops the edges on phones; everything important sits inside the central 1200 px. The strapline is in the band rather than the logo so it is not shown twice. |
| LinkedIn profile image | `linkedin-profile.html` | `GBS_HORIZON_SOCIAL_LINKEDIN-PROFILE_400x400_v1.0.png` | 400 x 400 | The square avatar on sage (`GBS_HORIZON_AVATAR_SQUARE_ON-SAGE`). Also valid for other platforms that want a square avatar. |
| Post template | `post-template.html` | `GBS_HORIZON_SOCIAL_POST-TEMPLATE_1080x1080_v1.0.png` | 1080 x 1080 | Sage panel with reversed logo, [TOPIC] eyebrow, off-white lower area with [Headline] and [Supporting line], web address and bars motif. Replace the bracketed text in the HTML and re-render; delete the grey template note before publishing. |
| Story template | `story-template.html` | `GBS_HORIZON_SOCIAL_STORY-TEMPLATE_1080x1920_v1.0.png` | 1080 x 1920 | Same system in portrait. Top and bottom 250 px are left for app controls. |
| Open Graph / link preview | `og-image.html` | `GBS_HORIZON_SOCIAL_OG-IMAGE_1200x630_v1.0.png` | 1200 x 630 | Primary logo with strapline centred on off-white, web address, sage base rule with a red tip. Upload to the website as the default `og:image`. |

Copy rules apply: UK English, no superlatives, no client names or statistics unless evidenced, no emojis. Headlines in Montserrat 700 sage, supporting lines in Inter, red for the web address and pipes only.
