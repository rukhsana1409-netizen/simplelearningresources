import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import test from "node:test";
import vm from "node:vm";


const buildClient = async () => {
  const source = await readFile(new URL("../../../download-analytics.js", import.meta.url), "utf8");
  const beacons = [];
  let clickHandler;
  const context = {
    Blob,
    URL,
    URLSearchParams,
    fetch: async () => new Response(null, {status: 204}),
    navigator: {sendBeacon: (_url, body) => { beacons.push(body); return true; }},
    window: {
      location: {
        href: "https://simplelearningresources.com/resources/pronouns/",
        origin: "https://simplelearningresources.com",
        pathname: "/resources/pronouns/",
        search: "",
      },
      worksheetResourcesById: {
        pronouns: {pdfUrl: "https://assets.simplelearningresources.com/worksheets/grade-1/reading/pronouns/pronouns.pdf?download=1"},
      },
    },
    document: {addEventListener: (name, handler) => { if (name === "click") clickHandler = handler; }},
  };
  vm.runInNewContext(source, context);
  return {
    beacons,
    click: link => clickHandler({target: {closest: selector => selector === "a" ? link : null}}),
  };
};

const link = (href, {download = false, classes = []} = {}) => ({
  href,
  hasAttribute: name => name === "download" && download,
  matches: selector => selector.split(",").some(candidate => classes.includes(candidate.trim().replace(/^[.#]/, ""))),
});

test("preview opens and closes do not create download events", async () => {
  const client = await buildClient();
  client.click(link("https://assets.simplelearningresources.com/worksheets/grade-1/reading/pronouns/pronouns/page-01.pdf", {
    classes: ["resource-preview-link"],
  }));
  assert.equal(client.beacons.length, 0);
});

test("intentional PDF controls emit distinct v2 download events", async () => {
  const client = await buildClient();
  client.click(link("https://assets.simplelearningresources.com/worksheets/grade-1/reading/pronouns/pronouns/page-01.pdf?download=1", {
    download: true,
    classes: ["page-download"],
  }));
  client.click(link("https://assets.simplelearningresources.com/worksheets/grade-1/reading/pronouns/pronouns.pdf?download=1", {
    download: true,
    classes: ["resource-primary-action"],
  }));
  client.click(link("https://assets.simplelearningresources.com/worksheets/grade-1/reading/pronouns/pronouns-parent-guide.pdf?download=1", {
    download: true,
    classes: ["answer-key-download"],
  }));
  assert.equal(client.beacons.length, 3);
  const events = await Promise.all(client.beacons.map(body => body.text().then(JSON.parse)));
  assert.deepEqual(events.map(event => event.downloadType), ["page-download", "pack-download", "supporting-download"]);
  assert.ok(events.every(event => event.version === 2 && event.resourceId === "pronouns"));
});
