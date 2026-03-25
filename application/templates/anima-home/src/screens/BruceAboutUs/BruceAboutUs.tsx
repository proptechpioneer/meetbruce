import { LeaseComplianceVerificationSection } from "./sections/LeaseComplianceVerificationSection";
import { MainHeaderSection } from "./sections/MainHeaderSection";
import { MaintenanceIssuesSection } from "./sections/MaintenanceIssuesSection";
import { RentFairnessSection } from "./sections/RentFairnessSection";
import { RentersRightsDetailsSection } from "./sections/RentersRightsDetailsSection";
import { RentersRightsOverviewSection } from "./sections/RentersRightsOverviewSection";
import { SiteFooterSection } from "./sections/SiteFooterSection";
import { TenantChatSupportSection } from "./sections/TenantChatSupportSection";

export const BruceAboutUs = (): JSX.Element => {
  return (
    <div
      className="bg-white w-full relative mx-auto min-h-screen"
      style={{ minHeight: "6200px" }}
      data-model-id="28:209"
    >
      <MainHeaderSection />
      <RentersRightsOverviewSection />
      <RentersRightsDetailsSection />
      <RentFairnessSection />
      <MaintenanceIssuesSection />
      <LeaseComplianceVerificationSection />
      <TenantChatSupportSection />
      <SiteFooterSection />
    </div>
  );
};
