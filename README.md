# JoaoCostaIFG wiki

[Access the Wiki here](https://wiki.joaocosta.dev).

You can read my blog post about it [here](https://joaocosta.dev/blog/14/using-joplin-to-publish-a-wiki).

## What/Why

This is my Wiki, which basically means a part of my personal notes that I decided to make public. I used to use dedicated wiki software. Started with [DokuWiki](https://www.dokuwiki.org/dokuwiki), then moved to [Wiki.js](https://js.wiki/). The problem was that reaching out to the wiki to take notes broke my workflow, so I didn't write much. At the same time I was trying to settle on a note taking software. I ended up choosing [Joplin](https://joplinapp.org/).

Joplin fits my use cases nicely:

- Allows me to take notes in markdown format.
- Has self-hosted sync options (bonus by being builtin).
- Allows me to have a shared notebook with my partner.
- Allows me to publish notes aka my personal wiki (using [Joplin Server](https://github.com/laurent22/joplin/blob/dev/packages/server/README.md)).

## How

Joplin allows me to publish notes (make them publicly viewable), but I wanted to publish an entire directory/notebook (my wiki). For this reason I went with a slightly different approach. I use a Github action to fetch my Wiki notebook using the [joplin cli](https://joplinapp.org/help/apps/terminal/) and export the contents as markdown files. There is another action that takes this markdown files and builds the Wiki using [mdBook](https://rust-lang.github.io/mdBook/).

In other words:

- I write in my notetaking app (Joplin) inside a Wiki notebook (directory).
- Github fetches these notes and exports them as markdown files.
- An intermediate step builds the Wiki summary (a sitemap needed by mdBook).
- Lastly, Github builds and publishes the Wiki with Github pages.

This happens once a day at midnight (UTC). The contents of the repo are something like a daily snapshot of the my Wiki notebook.

## Want to use this?

- Fork the repo
- Set the following Github secrets (for the action):
  - `JOPLIN_PATH` - your Joplin server instance URL. Something like `https://joplin.myserver.com`
  - `JOPLIN_USER` - the Joplin user that is gonna be used to fetch the contents. I created a user for this with whom I share the Wiki notebook.
  - `JOPLIN_PASSWORD` - the password for the Joplin user.

The step that builds the mdBook is on a [separate action](./.github/workflows/mdbook.yml). If you want to build another kind of site, for example a personal blog, you can change this action to build something else. There's a bunch of Github actions already setup for that.

## License

Code is MIT.
Wiki content is [Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)
