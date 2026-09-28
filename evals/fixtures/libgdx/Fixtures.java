import com.badlogic.gdx.*;
import com.badlogic.gdx.assets.*;
import com.badlogic.gdx.assets.loaders.*;
import com.badlogic.gdx.files.FileHandle;
import com.badlogic.gdx.graphics.*;
import com.badlogic.gdx.graphics.g2d.Batch;
import com.badlogic.gdx.scenes.scene2d.*;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import com.badlogic.gdx.utils.*;
import com.badlogic.gdx.utils.viewport.ScreenViewport;
import com.badlogic.gdx.math.Vector2;
import java.io.File;
import java.lang.reflect.Proxy;
import java.util.*;

public class Fixtures {
  @SuppressWarnings("unchecked")
  static <T> T stub(Class<T> c, Map<String,Object> ret) {
    return (T) Proxy.newProxyInstance(c.getClassLoader(), new Class[]{c}, (p, m, a) -> {
      if (ret.containsKey(m.getName())) return ret.get(m.getName());
      Class<?> r = m.getReturnType();
      if (r == boolean.class) return false; if (r == int.class) return 0; if (r == float.class) return 0f;
      if (r == long.class) return 0L; if (r == double.class) return 0d; return null;
    });
  }
  static void bootGdx() {
    Gdx.app = stub(Application.class, Map.of());
    Gdx.graphics = stub(Graphics.class, Map.of("getWidth", 800, "getHeight", 600, "getBackBufferWidth", 800, "getBackBufferHeight", 600));
    Gdx.gl = Gdx.gl20 = stub(com.badlogic.gdx.graphics.GL20.class, Map.of());
    Gdx.input = stub(Input.class, Map.of());
  }

  static int atlasLoads = 0, atlasDisposes = 0;
  static class FakeAtlas implements Disposable { boolean disposed; public void dispose(){ disposed = true; atlasDisposes++; } }
  static class FakeAtlasLoader extends SynchronousAssetLoader<FakeAtlas, FakeAtlasLoader.P> {
    static class P extends AssetLoaderParameters<FakeAtlas> {}
    FakeAtlasLoader(FileHandleResolver r){ super(r); }
    public FakeAtlas load(AssetManager am, String f, FileHandle h, P p){ atlasLoads++; return new FakeAtlas(); }
    public Array<AssetDescriptor> getDependencies(String f, FileHandle h, P p){ return null; }
  }
  static AssetManager newAssets() {
    FileHandleResolver res = n -> new FileHandle(new File("/tmp/" + n));
    AssetManager am = new AssetManager(res, false);
    am.setLoader(FakeAtlas.class, new FakeAtlasLoader(res));
    atlasLoads = 0; atlasDisposes = 0;
    return am;
  }
  static abstract class BaseScreen implements Screen {
    public void render(float d){} public void resize(int w,int h){} public void pause(){} public void resume(){} public void dispose(){}
    public void show(){} public void hide(){}
  }
  static class MenuScreen extends BaseScreen {
    AssetManager a; boolean unloadOnHide; MenuScreen(AssetManager a, boolean u){this.a=a; unloadOnHide=u;}
    public void show(){ a.get("ui.atlas", FakeAtlas.class); }
    public void hide(){ if (unloadOnHide) a.unload("ui.atlas"); }
  }
  static class GameScreen extends BaseScreen {
    AssetManager a; boolean selfLoad; GameScreen(AssetManager a, boolean s){this.a=a; selfLoad=s;}
    public void show(){ if (selfLoad) { a.load("ui.atlas", FakeAtlas.class); a.finishLoading(); } a.get("ui.atlas", FakeAtlas.class); }
  }
  static String tryTransition(String label, AssetManager am, boolean unloadOnHide, int preRefs, boolean gameSelfLoad, int cycles) {
    Game g = new Game(){ public void create(){} };
    for (int i = 0; i < preRefs; i++) am.load("ui.atlas", FakeAtlas.class);
    am.finishLoading();
    String result = "OK";
    try {
      for (int c = 0; c < cycles; c++) {
        g.setScreen(new MenuScreen(am, unloadOnHide));
        g.setScreen(new GameScreen(am, gameSelfLoad));
      }
    } catch (Exception e) { result = "ERRO: " + e.getMessage(); }
    return String.format("%-58s -> %-34s loads=%d disposes=%d isLoaded=%b refs=%s",
      label, result, atlasLoads, atlasDisposes, am.isLoaded("ui.atlas"), am.isLoaded("ui.atlas") ? String.valueOf(am.getReferenceCount("ui.atlas")) : "-");
  }

  static class FakeViewport extends ScreenViewport {
    @Override public void update(int w, int h, boolean c){ setScreenBounds(0,0,w,h); setWorldSize(w,h); }
    @Override public Vector2 unproject(Vector2 v){ v.y = 600 - v.y; return v; }
  }
  static Batch batchStub() { return stub(Batch.class, Map.of()); }
  static Map<Integer,Integer> hits = new TreeMap<>();
  static class InventoryScreen extends BaseScreen {
    InputMultiplexer mux; boolean fixRemove; String variant; Stage stage;
    InventoryScreen(InputMultiplexer m, boolean fix, String v){mux=m; fixRemove=fix; variant=v;}
    public void show(){
      stage = new Stage(new FakeViewport(), batchStub());
      final int id = System.identityHashCode(stage);
      Actor a = new Actor(); a.setBounds(100, 100, 200, 100);
      if (variant.equals("ClickListener")) a.addListener(new ClickListener(){ public void clicked(InputEvent e,float x,float y){ hits.merge(id,1,Integer::sum);} });
      else a.addListener(new InputListener(){ public boolean touchDown(InputEvent e,float x,float y,int p,int b){ hits.merge(id,1,Integer::sum); return false; } });
      stage.addActor(a);
      mux.addProcessor(stage);
    }
    public void hide(){ if (fixRemove) mux.removeProcessor(stage); }
  }
  static String inventoryRun(String label, String variant, boolean fix, int opens) {
    hits.clear();
    InputMultiplexer mux = new InputMultiplexer();
    Game g = new Game(){ public void create(){} };
    InventoryScreen last = null;
    for (int i = 0; i < opens; i++) { last = new InventoryScreen(mux, fix, variant); g.setScreen(last); g.setScreen(new BaseScreen(){}); }
    last = new InventoryScreen(mux, fix, variant); g.setScreen(last);
    int visibleId = System.identityHashCode(last.stage);
    hits.clear();
    mux.touchDown(150, 450, 0, 0); mux.touchUp(150, 450, 0, 0);
    int total = hits.values().stream().mapToInt(Integer::intValue).sum();
    return String.format("%-44s processors=%d  acoes_no_clique=%d  recebidas_pela_tela_visivel=%d  (stages distintos que agiram=%d)",
      label, mux.getProcessors().size, total, hits.getOrDefault(visibleId, 0), hits.size());
  }

  public static void main(String[] args) throws Exception {
    bootGdx();
    System.out.println("=== CASO 1: asset compartilhado (AssetManager REAL do LibGDX) ===");
    System.out.println(tryTransition("A1 hide() faz unload, refs=1 (cenario do caso)", newAssets(), true, 1, false, 1));
    System.out.println(tryTransition("A2 hide() faz unload, ui.atlas carregado 2x (refs=2)", newAssets(), true, 2, false, 1));
    System.out.println(tryTransition("A3 idem A2, 3 ciclos menu->game (2o ciclo quebra?)", newAssets(), true, 2, false, 3));
    System.out.println(tryTransition("A4 correcao: dono unico, hide() NAO faz unload, 5 ciclos", newAssets(), false, 1, false, 5));
    System.out.println(tryTransition("A5 'remendo': GameScreen recarrega+finishLoading no show", newAssets(), true, 1, true, 5));
    { AssetManager am = newAssets(); am.load("ui.atlas", FakeAtlas.class); am.finishLoading();
      Game g = new Game(){ public void create(){} };
      g.setScreen(new MenuScreen(am,false)); g.setScreen(new GameScreen(am,false));
      am.unload("ui.atlas");
      System.out.println("A6 dono unico descarrega no shutdown -> isLoaded=" + am.isLoaded("ui.atlas") + " disposes=" + atlasDisposes); }

    System.out.println();
    System.out.println("=== CASO 2: InputMultiplexer + Stage REAIS do LibGDX (clique em (150,150) do stage) ===");
    for (String v : new String[]{"ClickListener","InputListener(touchDown->false)"}) {
      System.out.println("--- listener: " + v);
      String vv = v.startsWith("Click") ? "ClickListener" : "Input";
      for (int n : new int[]{0,1,2,3})
        System.out.println(inventoryRun("SEM correcao, reaberturas anteriores=" + n, vv, false, n));
      System.out.println(inventoryRun("COM removeProcessor no hide, reaberturas=3", vv, true, 3));
    }
    { InputMultiplexer mux = new InputMultiplexer(); Stage s = new Stage(new FakeViewport(), batchStub());
      mux.addProcessor(s); s.dispose();
      System.out.println("\nStage.dispose() remove do multiplexer? contem=" + mux.getProcessors().contains(s, true)); }
    { Game g = new Game(){ public void create(){} }; final boolean[] disposed = {false};
      Screen a = new BaseScreen(){ public void dispose(){ disposed[0]=true; } };
      g.setScreen(a); g.setScreen(new BaseScreen(){});
      System.out.println("Game.setScreen dispoe a tela antiga? " + disposed[0]); }
    System.exit(0);
  }
}
