const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const readmePath = path.join(root, "README.md");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function replaceBlock(content, markerName, nextBlock) {
  const start = `<!-- ${markerName}:START -->`;
  const end = `<!-- ${markerName}:END -->`;
  const regex = new RegExp(`${escapeRegex(start)}[\\s\\S]*?${escapeRegex(end)}`);

  if (!regex.test(content)) {
    throw new Error(`Missing README block markers for ${markerName}`);
  }

  return content.replace(regex, `${start}\n${nextBlock.trim()}\n${end}`);
}

function renderStack(stack = []) {
  return stack.map((item) => `<code>${escapeHtml(item)}</code>`).join(" &middot; ");
}

function renderCurrentFocus() {
  const focus = readJson("data/current-focus.json");

  const rows = focus
    .map((item) => {
      const name = escapeHtml(item.name);
      const status = escapeHtml(item.status);
      const link = item.link
        ? `<a href="${escapeHtml(item.link)}"><strong>${name}</strong></a>`
        : `<strong>${name}</strong>`;

      return `
<tr>
  <td width="28%" valign="top">${link}</td>
  <td width="72%" valign="top">${status}</td>
</tr>`;
    })
    .join("\n");

  return `
### Currently Building

<table>
${rows}
</table>`;
}

function renderProjects() {
  const projects = readJson("data/projects.json");

  const rows = projects
    .map((project) => {
      const name = escapeHtml(project.name);
      const description = escapeHtml(project.description);
      const live = project.live
        ? `<a href="${escapeHtml(project.live)}">Live</a>`
        : "";
      const repo = project.repo
        ? `<a href="${escapeHtml(project.repo)}">Repo</a>`
        : "";
      const links = [live, repo].filter(Boolean).join(" &middot; ") || "Private";

      return `
<tr>
  <td valign="top">
    <strong>${name}</strong><br/>
    <sub>${description}</sub><br/><br/>
    ${renderStack(project.stack)}
    <br/><br/>
    ${links}
  </td>
</tr>`;
    })
    .join("\n");

  return `
## Featured Systems

<table>
${rows}
</table>`;
}

function renderShipLog() {
  const logs = readJson("data/ship-log.json");

  const rows = logs
    .map((item) => {
      return `
<tr>
  <td width="18%" valign="top"><code>${escapeHtml(item.date)}</code></td>
  <td width="82%" valign="top">
    <strong>${escapeHtml(item.title)}</strong><br/>
    <sub>${escapeHtml(item.detail)}</sub>
  </td>
</tr>`;
    })
    .join("\n");

  return `
## Recent Ship Log

<table>
${rows}
</table>`;
}

function main() {
  let readme = fs.readFileSync(readmePath, "utf8");

  readme = replaceBlock(readme, "CURRENT_FOCUS", renderCurrentFocus());
  readme = replaceBlock(readme, "FEATURED_PROJECTS", renderProjects());
  readme = replaceBlock(readme, "SHIP_LOG", renderShipLog());

  fs.writeFileSync(readmePath, readme);
  console.log("Profile README updated from data files.");
}

main();
