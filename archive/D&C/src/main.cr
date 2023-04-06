require "commander"
require "./ssrp.cr"

cli = Commander::Command.new do |cmd|
  cmd.use  = "ssrp"
  cmd.long = "String-site removal problem implementation."

  cmd.flags.add do |flag|
    flag.name        = "file"
    flag.short       = "-f"
    flag.long        = "--file"
    flag.default     = "input.txt"
    flag.description = "The name of a file including strings;"
  end 

  cmd.flags.add do |flag|
    flag.name        = "knum"
    flag.short       = "-k"
    flag.long        = "--knum"
    flag.default     = 2
    flag.description = "The number of columns to remove;"
  end

  cmd.run do |options, arguments|
    Ssrp.mainProcedure options.string["file"], options.int["knum"].to_i32
  end
end

Commander.run(cli, ARGV)
