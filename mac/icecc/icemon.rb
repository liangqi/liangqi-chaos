require 'formula'

class Icemon < Formula
  homepage 'https://github.com/icecc/icemon'
  url 'https://codeload.github.com/liangqi/icemon/zip/master'
  sha1 'd1c09a90c5d84e92dd9a4413d50501b15771230a'
  version '2.9.90-liang'

  depends_on 'cmake' => :build
  depends_on 'qt'

  def install
    system "cmake", ".", *std_cmake_args
    system "make"
    system "make", "install"
  end
end
