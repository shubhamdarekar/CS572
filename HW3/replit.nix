{ pkgs }: {
    deps = [
      pkgs.hadoop_3_2
      pkgs.unzip
      pkgs.wget
        pkgs.imagemagick6_light
        pkgs.graalvm17-ce
        pkgs.maven
        pkgs.replitPackages.jdt-language-server
        pkgs.replitPackages.java-debug
    ];
}