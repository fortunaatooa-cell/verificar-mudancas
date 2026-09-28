#!/usr/bin/env bash
# Reproduz os casos LibGDX usando uma revisão fixa do framework.
# Requer JDK 17+, git e acesso ao GitHub.
set -euo pipefail

LIBGDX_REF="${LIBGDX_REF:-e1d69884015ca19061647505f9509db34df5cc82}"
W="${1:-./lg-work}"
mkdir -p "$W"
W="$(cd "$W" && pwd)"
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$W"

if [ ! -d src/.git ]; then
  rm -rf src
  git clone -q --filter=blob:none --no-checkout https://github.com/libgdx/libgdx.git src
fi

git -C src fetch -q --depth 1 origin "$LIBGDX_REF"
git -C src sparse-checkout init --cone >/dev/null
git -C src sparse-checkout set gdx/src
git -C src checkout -q --detach "$LIBGDX_REF"

ACTUAL_REF="$(git -C src rev-parse HEAD)"
if [ "$ACTUAL_REF" != "$LIBGDX_REF" ]; then
  echo "ERRO: revisão inesperada do LibGDX: $ACTUAL_REF" >&2
  exit 1
fi

echo "LibGDX ref: $ACTUAL_REF"

rm -rf stubs out files.txt
mkdir -p stubs/com/badlogic/gdx/utils out
cat > stubs/com/badlogic/gdx/utils/Os.java <<'J'
package com.badlogic.gdx.utils;
public enum Os { Windows, Linux, MacOsX, Android, IOS }
J
cat > stubs/com/badlogic/gdx/utils/SharedLibraryLoader.java <<'J'
package com.badlogic.gdx.utils;
public class SharedLibraryLoader {
  public static Os os = Os.Linux;
  public static boolean isWindows=false,isLinux=true,isMac=false,isIos=false,isAndroid=false,isARM=false,is64Bit=true;
  public static String abi="", architecture="x86_64";
  public SharedLibraryLoader(){}
  public void load(String n){}
}
J
find src/gdx/src stubs -name '*.java' > files.txt
JAVAC="javac"
command -v javac >/dev/null || JAVAC="java -m jdk.compiler/com.sun.tools.javac.Main"
$JAVAC -nowarn -encoding UTF-8 -d out @files.txt
java -cp out "$HERE/Fixtures.java"
