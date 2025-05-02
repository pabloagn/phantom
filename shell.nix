{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    # Node.js and package managers
    nodejs_20
    nodePackages.pnpm
    
    # Development tools
    git
    nodePackages.typescript
    nodePackages.typescript-language-server
    
    # Libraries needed for Sharp and other native dependencies
    vips
    pkg-config
    
    # Common build dependencies
    gnumake
    gcc
    
    # Image processing libraries that Sharp depends on
    libjpeg
    libpng
    libwebp
    
    # For Canvas if needed
    cairo
    pango
    librsvg
  ];

  shellHook = ''
    export PATH="$PWD/node_modules/.bin:$PATH"
    # Make libraries available to Sharp
    export PKG_CONFIG_PATH="${pkgs.vips}/lib/pkgconfig:$PKG_CONFIG_PATH"
    export LD_LIBRARY_PATH="${pkgs.vips}/lib:$LD_LIBRARY_PATH"
    
    echo "Enhanced Next.js development environment ready!"
    echo "Node version: $(node -v)"
    echo "PNPM version: $(pnpm -v)"
  '';
}
