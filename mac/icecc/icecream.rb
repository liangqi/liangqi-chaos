require 'formula'

class Icecream < Formula
  homepage 'https://github.com/icecc/icecream'
  url 'https://codeload.github.com/liangqi/icecream/zip/master'
  sha1 '32474e44ef4f0d7e26cc237ca0c52ab230b2cf8e'
  version '1.0-liang'

  depends_on 'automake'
  depends_on 'libtool'
  depends_on 'docbook2x'

  def install
    system "./autogen.sh"
    system "./configure", "--disable-debug", "--disable-dependency-tracking",
                          "--enable-clang-wrappers",
                          "--prefix=#{prefix}"
    system "make"
    system "make", "install"
  end
end
