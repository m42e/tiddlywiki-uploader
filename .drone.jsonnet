[
  { 
    kind: "pipeline",
    name: "default",

    steps: [
      {
        name: "docker",
        image: "plugins/docker",
        settings: {
          registry: "registry.d1v3.de",
          repo: "registry.d1v3.de/tiddlywiki-upload",
          username: { from_secret: "docker_username"},
          password: { from_secret: "docker_password" },
        },
      tags: "latest",
      auto_tag: "true",
      },
    ],
  },
]

