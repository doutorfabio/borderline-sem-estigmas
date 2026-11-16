import asyncio, json, edge_tts, os, sys
LINES = [
 ("L01","Te disseram que borderline nunca melhora?"),
 ("L02","Um estudo seguiu duzentas e noventa pessoas internadas com borderline."),
 ("L03","Por dezesseis anos."),
 ("L04","Nesse tempo, noventa e nove em cada cem ficaram dois anos ou mais sem o diagnóstico."),
 ("L05","O estudo também mediu trabalho ou estudo constante."),
 ("L06","E ter ao menos um amigo ou parceiro próximo."),
 ("L07","Isso, com os sintomas em baixa, chegou para sessenta em cada cem."),
 ("L08","E demorou mais."),
 ("L09","Os sintomas cederam para quase todos."),
 ("L10","Trabalho e vínculos levaram mais tempo."),
]
async def one(i,t):
    c = edge_tts.Communicate(t, "pt-BR-AntonioNeural", rate="+0%", proxy=os.environ.get("HTTPS_PROXY"), boundary="WordBoundary")
    words=[]
    with open(f"{i}.mp3","wb") as f:
        async for ch in c.stream():
            if ch["type"]=="audio": f.write(ch["data"])
            elif ch["type"]=="WordBoundary": words.append({"w":ch["text"],"s":ch["offset"]/1e7,"d":ch["duration"]/1e7})
    return words
async def main():
    out={}
    for i,t in LINES:
        out[i]={"text":t,"words":await one(i,t)}
    json.dump(out,open("words.json","w"),ensure_ascii=False,indent=1)
asyncio.run(main())
