// Filter the publication list by status. SPDX-License-Identifier: MIT
document$.subscribe(() => {
  const buttons = document.querySelectorAll(".lr-pub-filter")
  buttons.forEach(button => button.addEventListener("click", () => {
    const filter = button.dataset.filter
    buttons.forEach(other => other.classList.toggle("is-active", other === button))
    document.querySelectorAll(".lr-pub").forEach(item => {
      item.hidden = filter !== "all" && item.dataset.status !== filter
    })
    document.querySelectorAll(".lr-pub-year").forEach(section => {
      section.hidden = !section.querySelector(".lr-pub:not([hidden])")
    })
  }))
})
