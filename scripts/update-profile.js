const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const readmePath = path.join(root, 'README.md');

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), 'utf8'));
}

function replaceBlock(content, markerName, nextBlock) {
  const start = `<!-- ${markerName}:START -->`;
  const end = `<!-- ${markerName}:END -->`;
  const regex = new RegExp(`${escapeRegex(start)}[\\s\\S]*?${escapeRegex(end)}`);
  return content.replace(regex, `${start}\n${nextBlock.trim()}\n${end}`);
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function mdLink(label, url) {
  if (!url) return label;
  return `[${label}](${url})`;
}

function codeList(items) {
  return items.map((item) => `\`${item}\``).join(' · ');
}

function renderCurrentFocus() {
  const focus = readJson('data/current-focus.json');
  const rows = focus
    .map((item) => `| ${mdLink(item.name, item.link)} | ${item.status} |`)
    .join('\n');

  return `### Currently Building\n\n| System | Status |\n|---|---|\n${rows}`;
}

function renderProjects() {
  const projects = readJson('data/projects.json');
  const rows = projects
    .map((project) => {
      const links = [
        project.live ? `[Live](${project.live})` : '',
        project.repo ? `[Repo](${project.repo})` : '',
      ].filter(Boolean).join(' · ');

      return `| ${project.name} | ${project.description} | ${codeList(project.stack)} | ${links || 'Private'} |`;
    })
    .join('\n');

  return `## Featured Systems\n\n| Project | What it does | Stack | Links |\n|---|---|---|---|\n${rows}`;
}

function renderShipLog() {
  const logs = readJson('data/ship-log.json');
  const rows = logs
    .map((item) => `| ${item.date} | ${item.title} | ${item.detail} |`)
    .join('\n');

  return `## Recent Ship Log\n\n| Date | Shipment | Detail |\n|---|---|---|\n${rows}`;
}

function main() {
  let readme = fs.readFileSync(readmePath, 'utf8');

  readme = replaceBlock(readme, 'CURRENT_FOCUS', renderCurrentFocus());
  readme = replaceBlock(readme, 'FEATURED_PROJECTS', renderProjects());
  readme = replaceBlock(readme, 'SHIP_LOG', renderShipLog());

  fs.writeFileSync(readmePath, readme);
  console.log('Profile README updated from data files.');
}

main();
