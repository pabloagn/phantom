{
  description = "Phantom system development environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Node.js and package management
            nodejs_20
            nodePackages.npm
            nodePackages.yarn
            nodePackages.pnpm

            # Development tools
            nodePackages.typescript
            nodePackages.typescript-language-server
            nodePackages.eslint
            nodePackages.prettier

            # Database tools
            postgresql_15
            docker
            docker-compose

            # Build tools
            gnumake
            gcc
          ];

          shellHook = ''
            # Set environment variables for local development
            export PHANTOM_DEV=1
            export PATH="$PWD/node_modules/.bin:$PATH"
            
            # Welcome message
            echo "🌟 Welcome to the Phantom development environment!"
            echo "📚 Documentation: https://github.com/phantom/phantom"
            echo "🛠️  Type 'npm install' to install dependencies"
          '';
        };

        # NixOS module for the Phantom system
        nixosModules.phantom = import ./modules/phantom.nix;
        nixosModules.phantom-db = import ./modules/phantom-db.nix;
        nixosModules.phantomklange = import ./modules/phantomklange.nix;
      }
    );
}