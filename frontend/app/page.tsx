export default function HomePage() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <section className="mx-auto flex max-w-5xl flex-col gap-4 px-6 py-20">
        <p className="text-sm uppercase tracking-[0.2em] text-cyan-300">ReconCore</p>
        <h1 className="text-4xl font-semibold">Reconciliation and Data Quality Platform</h1>
        <p className="max-w-2xl text-slate-300">
          Dashboard shell is live. API connection, auth, connector sync pages, and reconciliation
          views are added in the next steps.
        </p>
      </section>
    </main>
  );
}

