import { continueRender, delayRender, staticFile } from "remotion";

export const TheBoldFont = `TheBoldFont`;

let loaded = false;

export const loadFont = async (): Promise<void> => {
  if (loaded) {
    return Promise.resolve();
  }

  const waitForFont = delayRender();

  loaded = true;

  const font = new FontFace(
    TheBoldFont,
    `url('${staticFile("theboldfont.ttf")}') format('truetype')`,
  );

  await font.load();
  document.fonts.add(font);

  continueRender(waitForFont);
};

// Anton: fonte condensada com acentos do português (ã, ç, é).
// TheBoldFont não tem esses caracteres.
export const Anton = `Anton`;

let antonLoaded = false;

export const loadAnton = async (): Promise<void> => {
  if (antonLoaded) {
    return Promise.resolve();
  }

  const waitForFont = delayRender();

  antonLoaded = true;

  const font = new FontFace(
    Anton,
    `url('${staticFile("fonts/anton.woff2")}') format('woff2')`,
  );

  await font.load();
  document.fonts.add(font);

  continueRender(waitForFont);
};
