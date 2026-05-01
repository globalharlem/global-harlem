const fs = require('fs');
const path = require('path');

const BASE = '/Users/barona.carr/Desktop/global-harlem';
const STORIES_PATH = path.join(BASE, 'stories.json');
const HTML_PATH = path.join(BASE, 'intelligence.html');

// Map city names to the slugs used by the city filter pills
const CITY_SLUGS = {
  'Harlem': 'harlem',
  'Atlanta': 'atlanta',
  'Washington D.C.': 'washington',
  'Chicago': 'chicago',
  'Houston': 'houston',
  'London': 'london',
  'Accra': 'accra',
  'Lagos': 'lagos',
  'Toronto': 'toronto',
  'Kingston': 'kingston',
  'Paris': 'paris',
};

function citySlug(city) {
  return CITY_SLUGS[city] || city.toLowerCase().replace(/[^a-z]/g, '');
}

function buildCard(story) {
  const slug = citySlug(story.city);
  return `        <div class="story-card" data-city="${slug}">
          <p class="story-city">${story.city}</p>
          <h3 class="story-headline">${story.title}</h3>
          <p class="story-summary">${story.summary}</p>
          <a class="story-link" href="${story.link}" target="_blank" rel="noopener">Read more</a>
        </div>`;
}

function buildColumn(label, stories) {
  const cards = stories.slice(0, 3).map(buildCard).join('\n\n');
  return `      <!-- ${label.toUpperCase()} COLUMN -->
      <div class="story-column">
        <p class="story-column-label">${label}</p>

${cards}
      </div>`;
}

// Read data
const data = JSON.parse(fs.readFileSync(STORIES_PATH, 'utf8'));
let html = fs.readFileSync(HTML_PATH, 'utf8');

// Group by pillar
const byPillar = { Legacy: [], Leadership: [], Ownership: [] };
data.stories.forEach(s => {
  if (byPillar[s.pillar]) byPillar[s.pillar].push(s);
});

// Build new grid content
const newGridContent = [
  buildColumn('Legacy', byPillar.Legacy),
  buildColumn('Leadership', byPillar.Leadership),
  buildColumn('Ownership', byPillar.Ownership),
].join('\n\n');

// Replace the contents of .stories-grid, anchored between the grid div and section 04 comment
html = html.replace(
  /(<div class="stories-grid">)[\s\S]*?(<\/div>\s*\n\s*<\/section>\s*\n\s*<!-- SECTION 04)/,
  `$1\n\n${newGridContent}\n\n    </div>\n  </section>\n\n  <!-- SECTION 04`
);

fs.writeFileSync(HTML_PATH, html, 'utf8');

console.log(`\nGlobal Harlem — Story Loader`);
console.log(`Updated: ${HTML_PATH}`);
console.log(`Source:  ${data.last_updated}`);
console.log(`─────────────────────────────`);
console.log(`  Legacy:     ${byPillar.Legacy.length} stories (showing 3)`);
console.log(`  Leadership: ${byPillar.Leadership.length} stories (showing 3)`);
console.log(`  Ownership:  ${byPillar.Ownership.length} stories (showing 3)`);
console.log(`  Total:      ${data.total_stories} stories`);
