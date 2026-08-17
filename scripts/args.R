#### shared CLI argument helper (port adaptation) ####
# The upstream scripts read parameters from the snakemake object; in this
# oxo-flow port the same values are passed as command line arguments.  This
# helper is sourced by every R script via its --file= command line entry.

# get the value of a --flag VALUE style argument (NULL if absent)
get_arg <- function(args, flag) {
  idx <- which(args == flag)
  if (length(idx) == 0) {
    return(NULL)
  }
  if (idx + 1 > length(args)) {
    return(NULL)
  }
  return(args[idx + 1])
}

# get a comma separated list argument (character(0) if absent)
get_arg_list <- function(args, flag) {
  val <- get_arg(args, flag)
  if (is.null(val) || nchar(val) == 0) {
    return(character(0))
  }
  unlist(strsplit(val, ",", fixed = TRUE))
}

# get all values after a --flag until the next --flag (multi-value args;
# the shell passes space-joined lists as separate argv entries)
get_arg_multi <- function(args, flag) {
  idx <- which(args == flag)
  if (length(idx) == 0) {
    return(character(0))
  }
  vals <- args[(idx[1] + 1):length(args)]
  if (length(vals) == 0) {
    return(character(0))
  }
  is_flag <- grepl("^--", vals)
  if (any(is_flag)) {
    vals <- vals[seq_len(which(is_flag)[1] - 1)]
  }
  vals
}
