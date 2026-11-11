import { createTimeline, Timeline } from "animejs";
import { useLayoutEffect, useRef } from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

type Select = (selector: string) => Element[];

// Ponte entre Anime.js e Remotion.
// A timeline nunca roda sozinha: a cada quadro ela é posicionada no tempo
// exato de useCurrentFrame(). Assim o preview, o scrub e o render final
// mostram sempre a mesma imagem.
//
// Uso:
//   const ref = useAnimeTimeline((tl, $) => {
//     tl.add($(".bloco"), { opacity: [0, 1], duration: 400 });
//   });
//   return <AbsoluteFill ref={ref}>...</AbsoluteFill>;
//
// Os seletores de $ procuram apenas dentro do elemento com a ref.
// A função build roda uma vez, na montagem.
export const useAnimeTimeline = <T extends HTMLElement = HTMLDivElement>(
  build: (tl: Timeline, $: Select) => void,
) => {
  const ref = useRef<T>(null);
  const timeline = useRef<Timeline | null>(null);
  const buildRef = useRef(build);
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  useLayoutEffect(() => {
    const root = ref.current;
    if (!root) {
      return;
    }

    const tl = createTimeline({ autoplay: false });
    buildRef.current(tl, (selector) =>
      Array.from(root.querySelectorAll(selector)),
    );
    timeline.current = tl;

    return () => {
      tl.revert();
      timeline.current = null;
    };
  }, []);

  useLayoutEffect(() => {
    timeline.current?.seek((frame / fps) * 1000, true);
  }, [frame, fps]);

  return ref;
};
