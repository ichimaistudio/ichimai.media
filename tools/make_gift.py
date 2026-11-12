"""返信特典「お店の紹介リール」を作る。
usage: python3 tools/make_gift.py <data.json> <out_dir>
data.json: {shopName, tag, area, catch:[2〜3行], points:[3つ], cta, palette:{bg,ink,accent,sub,orb1,orb2}}
出力: <out_dir>/reel.mp4（1080x1920・15秒・BGM付き）, cover.jpg, check_*.png（自己チェック用の静止画）
"""
import json, shutil, subprocess, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
work = out / "_work"; work.mkdir(exist_ok=True)
shutil.copy(root / "templates/gift_reel.html", work / "index.html")
(work / "data.js").write_text("window.DATA=" + json.dumps(data, ensure_ascii=False) + ";")

render = root / "tools/render.py"
for t in ["2.2", "5.6", "10.4", "14.2"]:
    subprocess.run([sys.executable, str(render), str(work / "index.html"), str(out / f"check_{t}.png"), "--still", t], check=True)
subprocess.run([sys.executable, str(render), str(work / "index.html"), str(work / "frames"), "15", "30"], check=True)
subprocess.run([sys.executable, str(root / "tools/music.py"), str(work / "music.wav"), "15", "0.5,3.3,7.0,8.1,9.2,11.8"], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "30", "-i", str(work / "frames/f%05d.png"), "-i", str(work / "music.wav"),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                "-shortest", "-movflags", "+faststart", str(out / "reel.mp4")], check=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out / "check_2.2.png"), "-q:v", "3", str(out / "cover.jpg")], check=True)
shutil.rmtree(work)
print("done", out / "reel.mp4")
