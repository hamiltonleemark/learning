cc_library(
    name = "hello-greet",
    srcs = ["hello-greet.cc"],
    hdrs = ["hello-greet.h"],
    visibility = ["//test:__pkg__"],
)

cc_binary(
    name = "hello-world",
    srcs = ["hello-world" + ".cc"],
    deps = [
        ":hello-greet",
        "//lib:hello-time",
    ],
)
