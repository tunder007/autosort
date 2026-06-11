/**
 * page.tsx — home route redirects to /sort.
 *
 * What it does:
 *   Server redirect so users land on the sort page.
 */
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/sort");
}
